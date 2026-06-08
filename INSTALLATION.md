# 📖 完整安装指南

**最后更新**：2026年6月  
**版本**：1.0  
**兼容性**：Windows 7+ / Mac OS 10.14+ / Linux (Ubuntu 18.04+)

---

## 目录

1. [一键版安装（推荐）](#一键版安装推荐)
2. [源码版安装（开发者）](#源码版安装开发者)
3. [API Key 配置](#api-key-配置)
4. [验证安装](#验证安装)
5. [常见问题](#常见问题)

---

## 🎁 一键版安装（推荐）

**最简单的方式 - 无需安装Python**

### Windows 用户

#### 系统要求
- Windows 7+
- **不需要Python**
- 网络连接

#### 安装步骤

**第1步：下载**
- 从 [Releases](../../releases) 页面下载 `AI-Study-Tool-v1.0-standalone-*-win64.zip`

**第2步：解压**
- 右键点击 zip 文件 → 解压到此处
- 或使用任何解压工具解压

**第3步：启动**
- 进入解压后的文件夹
- **双击 `start.bat`** 文件
- 系统自动启动，浏览器自动打开

**第4步：配置（首次运行）**
- 首次启动时系统会自动创建 `config.json`
- 编辑 `config.json`，找到 `"api_key"` 行
- 填入你的 DeepSeek API Key（获取方法见下文）
- 保存文件，重启 `start.bat`

✅ 完成！无需任何Python知识

### Mac 用户

#### 系统要求
- Mac OS 10.14+
- **不需要Python**
- 网络连接

#### 安装步骤

**第1步：下载**
- 从 [Releases](../../releases) 页面下载 `AI-Study-Tool-v1.0-standalone-*-macos.zip`

**第2步：解压**
- 在Finder中双击 zip 文件会自动解压

**第3步：启动**
```bash
# 打开终端
cd ~/Downloads/AI-Study-Tool-v1.0-standalone-*  # 根据实际文件夹名修改
bash start.sh
```

**第4步：配置（首次运行）**
- 首次启动时系统会自动创建 `config.json`
- 用文本编辑器打开 `config.json`
- 填入你的 DeepSeek API Key
- 保存文件，重新运行 `bash start.sh`

✅ 完成！

### Linux 用户

#### 系统要求
- Ubuntu 18.04+ 或其他Linux发行版
- **不需要Python**
- 网络连接

#### 安装步骤

**第1步：下载**
- 从 [Releases](../../releases) 页面下载 `AI-Study-Tool-v1.0-standalone-*-linux.zip`

**第2步：解压**
```bash
unzip AI-Study-Tool-v1.0-standalone-*.zip
cd AI-Study-Tool-v1.0-standalone-*
```

**第3步：启动**
```bash
bash start.sh
```

**第4步：配置（首次运行）**
- 首次启动时系统会自动创建 `config.json`
- 用文本编辑器打开 `config.json`
- 填入你的 DeepSeek API Key
- 保存文件，重新运行 `bash start.sh`

✅ 完成！

---

## 👨‍💻 源码版安装（开发者）

**如需修改代码或参与开发，请使用源码版**

### 系统要求

- **Python 3.8+**（必须）
- Git（可选，用于克隆）
- 代码编辑器（VS Code 推荐）
- 网络连接

### 检查Python

```bash
# 检查Python是否安装
python --version
# 或
python3 --version

# 应该显示：Python 3.8.x 或更高
```

**如果未安装**：
- Windows：访问 [Python官网](https://www.python.org/downloads/)，下载并安装，**勾选 "Add Python to PATH"**
- Mac：使用 Homebrew `brew install python3`
- Linux：使用包管理器 `apt install python3 python3-pip`

### Windows 源码版安装

```bash
# 1. 解压文件
# 右键 zip → 解压到此处

# 2. 打开命令行进入项目
cd C:\Users\YourName\Downloads\AI-Study-Tool\backend

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动系统
uvicorn main:app --host 127.0.0.1 --port 8000

# 5. 打开前端（新命令行/浏览器）
# 直接打开：frontend/index.html
```

### Mac 源码版安装

```bash
# 1. 解压文件
unzip AI-Study-Tool-v1.0-source-*.zip

# 2. 进入项目
cd AI-Study-Tool/backend

# 3. 安装依赖
pip3 install -r requirements.txt

# 4. 启动系统
python3 -m uvicorn main:app --host 127.0.0.1 --port 8000

# 5. 打开前端（新终端）
# 用浏览器打开：frontend/index.html
```

### Linux 源码版安装

```bash
# 1. 解压文件
unzip AI-Study-Tool-v1.0-source-*.zip

# 2. 进入项目
cd AI-Study-Tool/backend

# 3. 安装依赖
pip3 install -r requirements.txt

# 4. 启动系统
uvicorn main:app --host 127.0.0.1 --port 8000

# 5. 打开前端（新终端）
# 用浏览器打开：frontend/index.html
```

---

## 🔑 API Key 配置

系统需要 DeepSeek API Key 才能使用 AI 分析功能（标注和复习功能无需Key）

### 获取 API Key

1. 访问 [DeepSeek官网](https://platform.deepseek.com)
2. 点击"开始使用"或登录
3. 注册账户（邮箱或手机）
4. 进入 API 管理界面
5. 创建新的 API Key
6. 复制 Key（格式：`sk-xxxxxxx...`）

### 配置 Key

**方式1：编辑配置文件（推荐）**

首次运行后，系统会自动创建 `config.json` 文件

1. 用文本编辑器打开 `config.json`
2. 找到这一行：
   ```json
   "api_key": ""
   ```
3. 替换为：
   ```json
   "api_key": "sk-你的真实Key"
   ```
4. 保存文件
5. 重启系统

**方式2：环境变量（高级用户）**

```bash
# Windows (命令行)
set DEEPSEEK_API_KEY=sk-你的Key

# Mac/Linux
export DEEPSEEK_API_KEY=sk-你的Key
```

---

## ✅ 验证安装

启动系统后，检查以下几点：

### 1. 后端是否运行？
- 看是否有黑色终端窗口
- 或访问 `http://127.0.0.1:8000` (如果显示JSON数据，说明正常)

### 2. 前端是否加载？
- 浏览器是否打开了页面
- 页面是否显示"AI评论深度训练系统"标题

### 3. 数据库是否创建？
- 检查项目目录中是否有 `app.db` 文件
- 有表示数据库已创建，正常

### 4. 配置文件是否正确？
- 检查 `config.json` 中的 `api_key` 是否已填入
- 如果为空，AI 分析功能不可用（其他功能正常）

---

## 🐛 常见问题

### 步骤1：检查Python

```bash
python3 --version
# 应该显示 Python 3.8+
```

**如果未安装**（Ubuntu/Debian）：
```bash
sudo apt update
sudo apt install python3.8 python3-pip python3-venv
```

**Fedora/CentOS**：
```bash
sudo dnf install python3.8 python3-pip
```

### 步骤2：解压文件

```bash
unzip AI-Study-Tool-v1.0.zip
# 或
tar -xf AI-Study-Tool-v1.0.tar.gz
```

### 步骤3：进入项目目录

```bash
cd AI-Study-Tool/backend
```

### 步骤4：一键安装

```bash
bash start.sh
```

### 步骤5：配置API Key

```bash
nano config.json
```

找到并修改：
```json
"api_key": "sk-你的Key"
```

### 步骤6：重新启动

```bash
bash start.sh
```

---

## API Key 配置

### 获取API Key

1. **访问DeepSeek官网**：https://platform.deepseek.com

2. **注册账户**：
   - 使用邮箱注册
   - 验证邮箱
   - 完成身份验证

3. **创建API Key**：
   - 登录后，进入 API Management
   - 点击 Create New Key
   - 复制生成的Key（格式：sk-xxxxx...）

4. **充值余额**：
   - 进入Billing页面
   - 选择充值金额
   - 完成支付

### 配置方式A：配置文件（推荐）

```json
// backend/config.json
{
  "api_key": "sk-你的真实API Key"
}
```

**优点**：
- ✅ 一次配置，永久有效
- ✅ 所有用户都能使用
- ✅ 最安全

### 配置方式B：环境变量

```bash
# Windows (PowerShell)
$env:DEEPSEEK_API_KEY="sk-你的Key"

# Mac/Linux (Bash)
export DEEPSEEK_API_KEY="sk-你的Key"
```

**优点**：
- ✅ 避免在代码中暴露Key
- ✅ 便于CI/CD部署

### 配置方式C：前端输入（不推荐用于生产）

- 在网页上输入API Key
- 点击[保存秘钥]
- 每个浏览器各自保存
- 清空缓存会丢失

---

## 验证安装

### 验证1：检查依赖

```bash
# 激活虚拟环境后
pip list

# 应该看到以下包：
# - fastapi
# - uvicorn
# - requests
# - beautifulsoup4
# - pydantic
```

### 验证2：测试后端

```bash
# 在backend目录中
python -m uvicorn main:app --host 127.0.0.1 --port 8000

# 应该看到：
# INFO:     Application startup complete
# INFO:     Uvicorn running on http://127.0.0.1:8000
```

按 Ctrl+C 停止

### 验证3：测试爬虫

```bash
# 使用curl测试API
curl http://127.0.0.1:8000/api/articles

# 应该返回JSON格式的文章列表
```

### 验证4：测试AI分析

```bash
# 在前端网页上
1. 获取一篇文章
2. 输入API Key并保存
3. 点击[AI深度分析]
4. 应该在10-20秒后返回分析结果
```

---

## 常见问题

### Q1: Python未找到

```
错误：'python' 不是内部或外部命令
```

**解决**：
1. 重新安装Python，勾选"Add to PATH"
2. 重启电脑
3. 或使用 `python3` 代替 `python`

---

### Q2: 权限被拒绝（Mac/Linux）

```
错误：Permission denied: './start.sh'
```

**解决**：
```bash
chmod +x start.sh
bash start.sh
```

---

### Q3: 端口8000被占用

```
错误：Address already in use
```

**解决**：
1. 修改 config.json：
   ```json
   "port": 8001
   ```

2. 或杀死占用端口的进程：
   ```bash
   # Windows (PowerShell)
   netstat -ano | findstr :8000
   taskkill /PID 进程ID /F
   
   # Mac/Linux
   lsof -i :8000
   kill -9 PID
   ```

---

### Q4: API Key错误

```
错误：❌ 分析出错：API Key无效或已过期
```

**解决**：
1. 确认Key格式（应以sk-开头）
2. 检查DeepSeek账户是否有余额
3. Key是否已过期（从DeepSeek后台重新生成）
4. 检查Key中是否有多余的空格

---

### Q5: 无法连接到网络

```
错误：无法获取文章列表，请检查网络
```

**解决**：
1. 检查网络连接
2. 检查是否需要VPN（某些地区）
3. 人民网可能暂时不可用，稍后重试

---

### Q6: 数据库锁定错误

```
错误：sqlite3.OperationalError: database is locked
```

**解决**：
1. 关闭后端（Ctrl+C）
2. 稍等5秒
3. 重新启动
4. 如果仍然失败，删除 app.db 文件（会自动重建）

---

## 高级配置

### 修改爬虫源

编辑 `backend/config.json`：

```json
{
  "crawl_sources": [
    "http://opinion.people.com.cn/GB/436867/index.html",
    "http://opinion.people.com.cn/GB/8213/49160/49219/index.html"
  ]
}
```

### 修改复习间隔

```json
{
  "review_days": [1, 2, 4, 7, 15]
}
```

改为其他值，例如：
```json
{
  "review_days": [1, 3, 7, 14, 30]
}
```

### 修改超时时间

```json
{
  "timeout": 10
}
```

增加到20秒用于网络较慢的环境

### 修改后端监听地址

```json
{
  "host": "127.0.0.1",  // 仅本机访问
  "port": 8000
}
```

改为远程访问：
```json
{
  "host": "0.0.0.0",    // 允许远程访问
  "port": 8000
}
```

⚠️ **警告**：远程访问需要配置防火墙和身份验证！

---

## 卸载/删除

### Windows

```bash
# 1. 停止后端（关闭黑窗口）
# 2. 删除整个项目文件夹
del /s AI-Study-Tool
```

### Mac/Linux

```bash
rm -rf AI-Study-Tool
```

---

## 下一步

✅ **安装完成！**

现在你可以：
1. 获取文章并进行学习
2. 标注关键内容
3. 使用AI深度分析
4. 复习学习内容

💡 **建议**：
- 阅读 [快速开始指南](../QUICK_START.md)
- 查看 [完整项目文档](../README.md)
- 关注 [故障排查章节](../README.md#常见问题)

---

## 获取帮助

- 📖 查看README.md中的故障排查
- 🐛 报告bug或功能建议
- 💬 提出问题（提供详细的错误信息）

---

**祝安装顺利！如有问题，欢迎反馈。** 🎉
