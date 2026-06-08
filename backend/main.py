from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import requests
import random
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from config import (
    DB_PATH, API_KEY, CORS_ORIGINS, CRAWL_SOURCES, 
    REVIEW_DAYS, TIMEOUT, DEEPSEEK_API_URL, DEEPSEEK_MODEL
)

app = FastAPI()

# 允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB = DB_PATH

# 初始化数据库


def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        url TEXT UNIQUE,
        content TEXT,
        publish_date TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS highlights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id INTEGER,
        text TEXT,
        type TEXT,
        note TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id INTEGER,
        review_date TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS ai_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_id INTEGER UNIQUE,
    result TEXT
    )""")

    conn.commit()
    conn.close()


init_db()

# 爬虫逻辑


def crawl_list(url):
    try:
        r = requests.get(
            url, headers={"User-Agent": "Mozilla/5.0"}, timeout=TIMEOUT)
        r.encoding = "utf-8"
        soup = BeautifulSoup(r.text, "html.parser")
        links = soup.select("a")
        results = []
        for a in links:
            title = a.text.strip()
            href = a.get("href")
            if href and "html" in href and len(title) > 8:
                if not href.startswith("http"):
                    href = "http://opinion.people.com.cn" + href
                results.append({"title": title, "url": href})
        return results
    except:
        return []


def crawl_article(url):
    try:
        r = requests.get(
            url, headers={"User-Agent": "Mozilla/5.0"}, timeout=TIMEOUT)
        r.encoding = "utf-8"
        soup = BeautifulSoup(r.text, "html.parser")

        # 1. 尝试精确定位人民网正文所在的容器
        # 人民网正文通常在 id 为 ozoom 或 class 为 rm_content 的 div 中
        main_content = soup.find("div", id="ozoom") or soup.find(
            "div", class_="rm_content") or soup.find("div", class_="artical_con")

        if main_content:
            paragraphs = main_content.select("p")
        else:
            # 如果没找到容器，退回到抓取所有 p 标签
            paragraphs = soup.select("p")

        cleaned_paragraphs = []
        # 2. 设立“黑名单”关键词，包含这些词的段落直接扔掉
        blacklist = [
            "分享让更多人看到", "人民日报社概况", "关于人民网",
            "报社招聘", "招聘英才", "广告服务", "合作加盟",
            "版权服务", "数据服务", "网站声明", "网站律师",
            "信息保护", "联系我们", "违法和不良信息", "许可证",
            "京ICP备", "Copyright", "版权所有", "点击播报本文"
        ]

        for p in paragraphs:
            text = p.text.strip()
            # 过滤掉空行
            if not text:
                continue
            # 过滤掉包含黑名单词汇的行
            if any(word in text for word in blacklist):
                continue
            # 过滤掉字数太短且看起来像日期的行（可选）
            if len(text) < 10 and ("年" in text and "月" in text):
                continue

            cleaned_paragraphs.append(text)

        return "\n\n".join(cleaned_paragraphs)  # 用双换行符连接，排版更好看
    except Exception as e:
        print(f"抓取正文出错: {e}")
        return "正文抓取失败，请手动访问链接阅读。"


@app.get("/api/fetch")
def fetch():
    candidates = []
    for u in CRAWL_SOURCES:
        items = crawl_list(u)
        candidates.extend(items)

    if not candidates:
        raise HTTPException(400, "无法获取文章列表，请检查网络")

    # 随机选一篇
    chosen_item = random.choice(candidates)

    # 检查是否重复
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id, title, content FROM articles WHERE url=?",
              (chosen_item["url"],))
    exists = c.fetchone()

    if exists:
        conn.close()
        return {"id": exists[0], "title": exists[1], "content": exists[2]}

    # 抓取正文
    content = crawl_article(chosen_item["url"])
    date_str = datetime.now().strftime("%Y-%m-%d")

    c.execute("INSERT INTO articles (title,url,content,publish_date) VALUES (?,?,?,?)",
              (chosen_item["title"], chosen_item["url"], content, date_str))
    article_id = c.lastrowid

    # 生成复习计划
    for d in REVIEW_DAYS:
        rev_date = (datetime.now() + timedelta(days=d)).strftime("%Y-%m-%d")
        c.execute("INSERT INTO reviews (article_id,review_date) VALUES (?,?)",
                  (article_id, rev_date))

    conn.commit()
    conn.close()

    return {"id": article_id, "title": chosen_item["title"], "content": content}


class AnalyzeReq(BaseModel):
    article_id: int
    api_key: str = ""  # 空表示使用全局配置中的API Key
    content: str


@app.post("/api/analyze")
def analyze(req: AnalyzeReq):
    import json
    
    # 优先级：请求提供的Key > 全局配置的Key
    api_key_input = req.api_key.strip() if req.api_key else API_KEY
    
    if not api_key_input:
        return {
            "status": "error",
            "message": "未配置API Key。请在frontend/index.html中输入，或在backend/config.json中配置。"
        }
    
    print(f"正在使用的API Key前缀: {api_key_input[:5]}...")

    prompt = f"请作为申论专家，严谨分析文章。必须以JSON格式返回，包含三个字段：problems(数组), causes(数组), solutions(数组)。文章内容：{req.content}"

    try:
        headers = {
            "Authorization": f"Bearer {api_key_input}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": DEEPSEEK_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"}
        }

        binary_data = json.dumps(payload, ensure_ascii=False).encode('utf-8')

        res = requests.post(
            DEEPSEEK_API_URL,
            headers=headers,
            data=binary_data,
            timeout=60
        )

        # 如果返回了 401/402/404 等错误，会在这里直接抛出异常
        res.raise_for_status()

        ai_data = res.json()
        analysis_text = ai_data['choices'][0]['message']['content']

        # 保存到数据库
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO ai_analysis (article_id, result) VALUES (?, ?)",
                  (req.article_id, analysis_text))
        conn.commit()
        conn.close()

        return {"status": "success", "data": analysis_text}
    except Exception as e:
        # 如果报错了，打印出详细的响应内容，方便排查
        error_msg = str(e)
        if hasattr(e, 'response') and e.response is not None:
            error_msg += f" | 详情: {e.response.text}"
        print(f"AI分析错误详情: {error_msg}")
        return {"status": "error", "message": f"AI分析失败: {error_msg}"}


class HighlightReq(BaseModel):
    article_id: int
    text: str
    type: str
    note: str = ""  # 新增


@app.post("/api/highlight")
def highlight(req: HighlightReq):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO highlights (article_id,text,type,note) VALUES (?,?,?,?)",
              (req.article_id, req.text, req.type, req.note))
    conn.commit()
    conn.close()
    return {"ok": True}


@app.get("/api/articles")
def get_all_articles():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    # 按时间倒序排列，最近读的在最上面
    c.execute("SELECT id, title, publish_date FROM articles ORDER BY id DESC")
    data = [{"id": row[0], "title": row[1], "date": row[2]}
            for row in c.fetchall()]
    conn.close()
    return data


# 1. 增加删除接口


@app.delete("/api/article/{article_id}")
def delete_article(article_id: int):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("DELETE FROM articles WHERE id=?", (article_id,))
    c.execute("DELETE FROM highlights WHERE article_id=?", (article_id,))
    c.execute("DELETE FROM reviews WHERE article_id=?", (article_id,))
    c.execute("DELETE FROM ai_analysis WHERE article_id=?",
              (article_id,))  # 【新增】删掉这篇连带的 AI 笔记
    conn.commit()
    conn.close()
    return {"ok": True}

# 2. 修改获取单篇文章接口（增加批注逻辑）


@app.get("/api/article/{article_id}")
def get_single_article(article_id: int):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    # 获取文章
    c.execute("SELECT title, content FROM articles WHERE id=?", (article_id,))
    art = c.fetchone()
    # 获取标注
    c.execute(
        "SELECT text, type, note FROM highlights WHERE article_id=?", (article_id,))
    hls = [{"text": row[0], "type": row[1], "note": row[2]}
           for row in c.fetchall()]
    # 获取 AI 分析（新增）
    c.execute("SELECT result FROM ai_analysis WHERE article_id=?", (article_id,))
    ai_res = c.fetchone()

    conn.close()
    return {
        "title": art[0],
        "content": art[1],
        "highlights": hls,
        "ai_analysis": ai_res[0] if ai_res else None  # 如果有就传，没有传空
    }
