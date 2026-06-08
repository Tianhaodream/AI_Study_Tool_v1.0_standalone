# 🧠 AI 评论深度训练系统

一个融合**爬虫技术**、**AI分析**和**学习管理**的智能学习助手，帮助用户深度学习和分析新闻评论文章。

## 📋 项目概述

本系统用于申论/评论写作训练，通过以下特点提升学习效率：

- **自动获取**：从人民网评论栏目实时爬取最新文章
- **AI深度分析**：使用DeepSeek API进行结构化分析（问题→原因→对策）
- **个性化标注**：标记文章中的关键信息，支持添加个人笔记
- **智能复习**：自动生成基于遗忘曲线的复习计划
- **完整记录**：保存所有学习历史和分析结果，支持随时回顾

---

## 🏗️ 系统架构

```
AI_Study_Tool/
├── backend/
│   ├── main.py              # FastAPI后端服务
│   └── app.db               # SQLite数据库
├── frontend/
│   └── index.html           # 前端Web界面
├── 启动系统.bat              # 一键启动脚本（Windows）
└── README.md                # 本文件
```

### 技术栈

| 层级 | 技术 | 用途 |
|------|------|------|
| **前端** | HTML5 + Tailwind CSS + Vanilla JS | 响应式用户界面 |
| **后端** | FastAPI | RESTful API服务 |
| **数据库** | SQLite | 本地数据持久化 |
| **爬虫** | BeautifulSoup + Requests | 网页内容提取 |
| **AI** | DeepSeek API | 文章结构化分析 |

---

## 💾 数据库设计

### 表结构

#### 1. `articles` - 文章表
```
id(主键) | title | url | content | publish_date
```
存储爬取的文章内容

#### 2. `highlights` - 标注表
```
id | article_id | text | type | note
```
- `type`：问题(problem) / 原因(cause) / 对策(solution)
- `note`：用户自定义批注

#### 3. `reviews` - 复习计划表
```
id | article_id | review_date
```
使用间隔重复法：1天、2天、4天、7天、15天

#### 4. `ai_analysis` - AI分析结果表
```
id | article_id | result
```
存储JSON格式的AI分析结果（含问题、原因、对策）

---

## 🚀 快速开始

### ⚡ 最快方式（推荐小白用户）

无需安装Python，一键启动：

**Windows用户**：
1. 从 [Releases](../../releases) 下载 `AI-Study-Tool-v1.0-standalone-*.zip`
2. 解压到任意位置
3. 双击 `start.bat` 启动系统
4. 浏览器自动打开，按提示填入API Key即可使用

**Mac/Linux用户**：
1. 从 [Releases](../../releases) 下载对应版本
2. 解压后运行 `bash start.sh`
3. 浏览器自动打开，按提示填入API Key即可使用

### 📋 系统要求（一键版）

- Windows 7+ / Mac OS 10.14+ / Linux (Ubuntu 18.04+)
- **不需要安装Python**
- 网络连接（用于爬虫和AI分析）

---

## 🛠️ 开发者安装（源码版）

如需修改代码或参与开发，请参考以下步骤：

### 系统要求（源码版）

- **操作系统**：Windows/Mac/Linux
- **Python**：3.8+
- **网络**：需要访问人民网和DeepSeek API

### 环境配置

#### 1. 安装Python依赖

```bash
cd backend
pip install -r requirements.txt
```

#### 2. 获取DeepSeek API Key

1. 访问 [DeepSeek官网](https://platform.deepseek.com)
2. 注册账户并创建API Key
3. 保管好Key（系统默认内置一个试用Key，但建议替换为自己的）

#### 3. 启动系统

**Windows用户**（推荐）：
```bash
双击 启动系统.bat
```

该脚本会自动：
1. 启动FastAPI后端（端口8000）
2. 等待2秒
3. 在浏览器打开前端界面

**手动启动**：
```bash
# 终端1：启动后端
cd backend
uvicorn main:app --host 127.0.0.1 --port 8000

# 终端2：打开前端
直接在浏览器打开 frontend/index.html
```

---

## 🎯 功能详解

### 1️⃣ 获取今日文章

```
[获取今日文章] 按钮
  ↓
后端连接人民网爬虫源
  ↓
随机选择一篇未读文章
  ↓
提取正文内容（智能过滤广告/页脚）
  ↓
生成5个复习日期 (1,2,4,7,15天)
  ↓
前端显示文章内容
```

**爬虫特点**：
- 自动过滤人民网页脚、广告等干扰信息
- 支持两个评论栏目源
- 防重复：已读文章不再重复获取

### 2️⃣ 标注与笔记

支持三种标注类型，快速标记关键内容：

| 标注类型 | 颜色 | 用途 | 快捷键 |
|---------|------|------|--------|
| 🔴 问题 | 红色 | 标记文章描述的问题 | [标记问题] |
| 🟡 原因 | 黄色 | 标记导致问题的原因 | [标记原因] |
| 🟢 对策 | 绿色 | 标记解决问题的方案 | [标记对策] |

**操作流程**：
1. 选中文章中的文本
2. 点击对应标注按钮
3. 输入个人批注（可选）
4. 标注自动保存到数据库

悬停标注可显示批注内容。

### 3️⃣ AI深度分析

```
[AI深度分析] 按钮
  ↓
发送文章内容到DeepSeek
  ↓
AI申论专家角色分析
  ↓
返回JSON结构化结果
  ↓
前端展示：
  - 🚩 核心问题
  - 🔍 深度原因
  - 💡 应对对策
```

**提示**：
- 首次分析需要10-20秒，请耐心等待
- 需要有效的DeepSeek API Key和余额
- 分析结果自动保存，刷新页面可查看历史分析

### 4️⃣ 历史练习记录

底部显示所有已学习的文章列表：

- **点击标题**：加载该文章及所有标注和分析结果
- **点击删除**（🗑️）：彻底删除文章及其所有关联数据

---

## 🔌 API端点

### 后端API文档

#### 获取文章列表
```
GET /api/fetch
响应: { id, title, content }
```

#### 获取所有文章标题
```
GET /api/articles
响应: [ { id, title, date }, ... ]
```

#### 获取单篇文章详情
```
GET /api/article/{article_id}
响应: {
  title,
  content,
  highlights: [ { text, type, note }, ... ],
  ai_analysis: JSON字符串
}
```

#### 创建标注
```
POST /api/highlight
请求体: {
  article_id,
  text,
  type: "problem|cause|solution",
  note: ""
}
```

#### AI分析
```
POST /api/analyze
请求体: {
  article_id,
  content,
  api_key: "sk-..."
}
响应: { status, data: JSON }
```

#### 删除文章
```
DELETE /api/article/{article_id}
响应: { ok: true }
```

---

## ⚙️ 配置说明

### 前端配置

编辑 `frontend/index.html` 中的脚本部分：

```javascript
// 后端服务地址（默认本地8000端口）
const API_BASE = "http://localhost:8000"

// API Key本地存储
localStorage.setItem("apiKey", "your-deepseek-key")
```

### 后端配置

编辑 `backend/main.py` 中的常量：

```python
# 爬虫源URL
urls = [
    "http://opinion.people.com.cn/GB/436867/index.html",  # 评论
    "http://opinion.people.com.cn/GB/8213/49160/49219/index.html"  # 观点
]

# 复习间隔（天数）
review_days = [1, 2, 4, 7, 15]

# 默认API Key
DEFAULT_KEY = "sk-..."

# 数据库路径
DB = "app.db"
```

---

## 🐛 故障排查

### 问题1：启动脚本运行后黑窗口立即关闭

**原因**：后端服务启动失败
**解决**：
```bash
# 手动运行后端，查看错误信息
cd backend
uvicorn main:app --host 127.0.0.1 --port 8000
```

### 问题2：前端页面无法加载

**原因**：后端未启动或端口被占用
**解决**：
- 确认后端运行：`netstat -ano | findstr :8000`
- 若被占用，修改启动脚本中的端口号

### 问题3：抓取文章失败

**原因**：网络问题或人民网网站结构变化
**解决**：
- 检查网络连接
- 验证爬虫URL是否仍然有效
- 更新BeautifulSoup选择器

### 问题4：AI分析返回错误

**原因**：API Key无效或余额不足
**解决**：
1. 确认API Key正确性
2. 检查DeepSeek账户余额
3. 查看后端控制台的详细错误信息

### 问题5：数据库被锁定

**症状**：系统报告`database is locked`
**解决**：
```bash
# 删除旧数据库文件（谨慎操作）
rm backend/app.db
# 系统会自动重建
```

---

## 📊 学习流程示例

```
1. 点击[获取今日文章] → 系统随机获取一篇文章
                ↓
2. 阅读文章，选中关键文本
                ↓
3. 点击[标记问题/原因/对策] → 添加颜色标注和笔记
                ↓
4. 完成标注后，点击[AI深度分析]
                ↓
5. 查看AI结构化分析结果，对比自己的理解
                ↓
6. 系统自动生成复习计划（1,2,4,7,15天）
                ↓
7. 下次登陆时，点击历史记录复习该文章
                ↓
8. 重复复习直至掌握
```

---

## 🔒 安全建议

1. **API Key管理**
   - 不要在代码中硬编码个人Key
   - 使用环境变量或配置文件管理敏感信息
   - 定期轮换API Key

2. **数据隐私**
   - 数据仅存储在本地数据库（app.db）
   - 不上传到第三方服务器
   - 定期备份重要数据

3. **网络安全**
   - 仅在本地运行（localhost:8000）
   - 若需远程访问，配置HTTPS和认证
   - 启用CORS仅限必要的域名

---

## 📈 后续改进方向

### 短期计划
- [ ] 支持导入自定义文章源（URL、RSS订阅）
- [ ] 实现标注数据导出为PDF/Word
- [ ] 添加学习统计（完成率、掌握度评分）
- [ ] 支持深色模式

### 中期计划
- [ ] 基于用户标注的个性化复习算法
- [ ] 支持多用户账户体系
- [ ] 本地LLM模型集成（降低API成本）
- [ ] 移动端适配

### 长期计划
- [ ] 云同步（跨设备学习进度）
- [ ] 社区对标（与其他学习者比较分析）
- [ ] 智能题库生成（基于文章内容）
- [ ] 申论模拟考试系统

---

## 📝 许可证

本项目为学习研究用途，遵守相关法律法规。

---

## 👨‍💻 开发信息

### 核心模块说明

| 模块 | 文件 | 功能 |
|------|------|------|
| API服务 | `backend/main.py:@app.get("/api/fetch")` | 获取文章 |
| 爬虫 | `backend/main.py:crawl_article()` | 提取文章正文 |
| AI分析 | `backend/main.py:@app.post("/api/analyze")` | DeepSeek集成 |
| 前端 | `frontend/index.html` | 完整UI逻辑 |
| 标注系统 | `frontend/index.html:highlight()` | 文本标记功能 |

### 代码量统计
- **后端**：~320行 Python
- **前端**：~287行 HTML/JS
- **总计**：~600行核心代码

---

## 🤝 反馈与建议

如发现问题或有改进建议，欢迎提出！

---

**最后更新**：2026年6月
**版本**：1.0
**状态**：可正式使用 ✅
