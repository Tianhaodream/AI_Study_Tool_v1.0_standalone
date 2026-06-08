# 🚀 上传发布包到 GitHub Releases - 完整指南

你的发布包已经生成完毕！现在可以上传到 GitHub Releases 供用户下载。

---

## 📋 发布包清单

以下文件已经在 `releases/` 文件夹中准备好：

| 文件名 | 大小 | 说明 |
|-------|------|------|
| `AI-Study-Tool-v1.0-source-20260608.zip` | 0.03 MB | 📖 开发者版（源码） |
| `AI-Study-Tool-v1.0-standalone-20260608-win64.zip` | 30.12 MB | 🎁 用户版（一键启动，无需 Python） |
| `README.md` | - | 📝 发布说明 |

---

## 🎯 两种上传方式

### 方案 A：使用 GitHub 网页界面（最简单，推荐！）

**步骤 1：打开 GitHub Releases 页面**
```
访问: https://github.com/YOUR_USERNAME/YOUR_REPO/releases
替换 YOUR_USERNAME 和 YOUR_REPO 为你的真实信息
```

**步骤 2：创建新 Release**
- 点击 "Draft a new release"（或类似按钮）
- 选择 Tag 版本：`v1.0`
- 标题：`AI 学习工具 v1.0 发布`
- 描述框复制以下内容：

```markdown
# AI 学习工具 v1.0 发布

## 📦 下载

### 对于普通用户（推荐）
- **AI-Study-Tool-v1.0-standalone-20260608-win64.zip** (30MB)
  - 包含完整的可执行程序
  - 无需安装 Python
  - Windows 10+ 用户可直接使用
  - 解压后双击《启动系统.bat》即可运行

### 对于开发者
- **AI-Study-Tool-v1.0-source-20260608.zip** (0.03MB)
  - 包含完整源代码
  - 可用于修改和二次开发
  - 需要 Python 环境

## 📖 使用指南
1. 下载对应版本
2. 解压到本地
3. **用户版**：双击《启动系统.bat》启动
4. **开发版**：参考 README.md 进行配置

## 📝 文档
- 📋 【打印版】AI学习工具使用指南.txt - 8 页快速指南
- 🚀 快速开始（小白版）.txt - 详细启动步骤
- 📖 小白使用说明.md - 4400 行完整手册

## ✨ 本版本特点
- ✅ 首次启动自动配置
- ✅ 相对路径支持，任意位置可启动
- ✅ 全中文界面和文档
- ✅ 本地数据存储，安全可靠
- ✅ 核心功能完整可用

## 🐛 遇到问题？
查看 【打印版】AI学习工具使用指南.txt 或 小白使用说明.md
```

**步骤 3：上传文件**
- 在描述框下方找到 "Attach binaries..."（附加二进制文件）
- 拖拽或点击选择以下文件：
  1. `AI-Study-Tool-v1.0-source-20260608.zip`
  2. `AI-Study-Tool-v1.0-standalone-20260608-win64.zip`

**步骤 4：发布**
- 勾选 "Set as the latest release"（设为最新版本）
- 点击 "Publish release"

✅ **完成！** 用户现在可以在 GitHub Releases 页面下载了

---

### 方案 B：使用 Git 命令行（适合经常发布的项目）

#### 前置条件
1. 已经在 GitHub 创建了仓库
2. 本地 Git 已配置

#### 步骤 1：配置 Git 远程（如果还没配置）

如果你还不知道仓库地址，可以这样找：
```
1. 登录 GitHub
2. 找到你的仓库
3. 点击 <> Code 按钮
4. 复制 HTTPS 或 SSH 地址
```

然后运行：
```bash
cd D:\AI_Study_Tool
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
# 或
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO.git
```

**验证配置：**
```bash
git remote -v
# 应该显示：
# origin  https://github.com/YOUR_USERNAME/YOUR_REPO.git (fetch)
# origin  https://github.com/YOUR_USERNAME/YOUR_REPO.git (push)
```

#### 步骤 2：提交代码到 GitHub

```bash
# 添加所有文件
git add .

# 提交更改
git commit -m "release: v1.0 发布 - 小白一键启动、完整文档"

# 推送到 GitHub
git push origin main
```

#### 步骤 3：创建 Release（使用 GitHub CLI）

首先安装 GitHub CLI：
```
https://cli.github.com/
```

然后创建 Release：
```bash
cd D:\AI_Study_Tool

# 登录 GitHub
gh auth login

# 创建 Release
gh release create v1.0 \
  --title "AI 学习工具 v1.0 发布" \
  --notes "首个完整发布版本，包含一键启动版和源码版本" \
  releases/AI-Study-Tool-v1.0-source-20260608.zip \
  releases/AI-Study-Tool-v1.0-standalone-20260608-win64.zip
```

✅ **完成！** Release 已创建并上传所有文件

---

## 🎓 如果还没有 GitHub 仓库？

### 快速创建流程

#### 1. 在 GitHub 创建新仓库
```
1. 访问 https://github.com/new
2. Repository name: AI_Study_Tool
3. Description: AI 学习工具 - 小白一键启动版
4. Public（公开） or Private（私密），任选
5. 不需要初始化 README（我们已有）
6. Create repository
```

#### 2. 配置本地 Git
```bash
cd D:\AI_Study_Tool

# 配置用户信息
git config user.name "Your Name"
git config user.email "your.email@example.com"

# 添加远程
git remote add origin https://github.com/YOUR_USERNAME/AI_Study_Tool.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

#### 3. 创建 Release
参考上方【方案 A】或【方案 B】的步骤

---

## 📊 发布后的用户使用流程

```
用户访问 GitHub
    ↓
点击 Releases 页面
    ↓
看到 v1.0 发布
    ↓
下载 AI-Study-Tool-v1.0-standalone-20260608-win64.zip
    ↓
解压到本地
    ↓
双击《启动系统.bat》
    ↓
浏览器自动打开，配置 API 密钥
    ↓
开始使用！✨
```

---

## ✅ 检查清单

上传前，请确认：

- [ ] 发布文件存在于 `releases/` 文件夹
- [ ] 源码版和用户版都已生成
- [ ] GitHub 仓库已创建
- [ ] 本地 Git 已配置（如使用命令行方式）
- [ ] Release 描述清晰，包含下载说明
- [ ] 用户版文件已上传到 Release 附件
- [ ] 开发者版文件已上传到 Release 附件

---

## 🚀 推荐工作流

如果你要频繁发布更新：

```bash
# 每次发布前，运行打包脚本
python release_all.py

# 提交代码
git add .
git commit -m "release: v1.1 更新说明"
git push origin main

# 创建 Release（使用网页或 gh CLI）
gh release create v1.1 \
  --notes "更新说明" \
  releases/AI-Study-Tool-v1.1-source-*.zip \
  releases/AI-Study-Tool-v1.1-standalone-*.zip
```

---

## 💡 额外建议

1. **定期更新**
   - 每个大功能完成后创建新 Release
   - 版本号遵循 semantic versioning (v1.0, v1.1, v2.0 等)

2. **更新文档**
   - 在 Release 描述中列出变更清单
   - 保持用户文档同步更新

3. **收集反馈**
   - 在 GitHub Issues 中接收用户反馈
   - 根据反馈快速迭代

4. **备份**
   - GitHub 会自动备份，无需担心丢失
   - 本地也保留 releases/ 文件夹副本

---

**祝发布顺利！如有任何问题，参考 GitHub 官方文档或提交 Issue。** 🎉
