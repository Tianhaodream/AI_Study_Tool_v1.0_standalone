# 🎯 用户安装快速参考卡

打印此页面贴在显示器上！

---

## ⚡ 三步快速开始

### 步骤1️⃣：检查Python

```bash
python --version
# 应该显示 Python 3.8+
# 若未安装，访问 https://www.python.org
```

### 步骤2️⃣：运行安装脚本

**Windows 用户**：
```
1. 右键点击 backend/install.bat
2. 选择 "打开"
3. 等待完成（会自动打开网页）
```

**Mac/Linux 用户**：
```bash
cd backend
bash start.sh
```

### 步骤3️⃣：配置API Key

编辑 `backend/config.json`，找到：
```json
"api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

替换为你的真实Key：
```json
"api_key": "sk-你的Key"
```

重新运行脚本启动。

---

## 🔑 快速获取API Key

1. 访问：https://platform.deepseek.com
2. 注册 → 登录 → 创建API Key
3. 复制Key → 粘贴到config.json
4. 充值余额

---

## 📱 首次使用

1. **获取文章**：点击 [获取今日文章]
2. **标注内容**：选择文本 → 点 [标记问题/原因/对策]
3. **AI分析**：点 [AI深度分析]（需要10-20秒）
4. **复习**：点下方的历史记录复习

---

## ⚠️ 常见问题速查

| 问题 | 解决方案 |
|------|--------|
| **Python找不到** | 重新安装Python，勾选"Add to PATH" |
| **权限被拒绝** | 在terminal运行：`chmod +x start.sh` |
| **端口被占用** | 改config.json的port为其他值 |
| **API Key错误** | 确认Key有效、账户有余额 |
| **网络错误** | 检查网络连接，可能需要VPN |
| **数据库锁定** | 关闭后端，删除app.db，重启 |

详细版本见：INSTALLATION.md

---

## 📞 获取帮助

1. 查看 `INSTALLATION.md` 完整指南
2. 查看 `QUICK_START.md` 快速教程
3. 查看 `README.md` 项目文档
4. 检查后端黑窗口的错误信息

---

## 🎓 学习流程

```
打开网页
  ↓
输入/粘贴API Key，点保存
  ↓
点[获取今日文章]
  ↓
阅读文章，标注关键内容
  ↓
点[AI深度分析]
  ↓
查看AI分析结果，对比自己的理解
  ↓
系统自动生成复习计划
  ↓
后续定期复习巩固
```

---

## 💾 文件说明

```
AI-Study-Tool/
├── backend/install.bat      ← Windows用户双击这个
├── backend/start.sh         ← Mac/Linux用户运行这个
├── backend/config.json      ← 编辑这个，填入API Key
├── frontend/index.html      ← 打开这个看网页
├── README.md                ← 完整文档
├── QUICK_START.md           ← 5分钟教程
└── INSTALLATION.md          ← 详细安装指南
```

---

## ✅ 安装检查清单

- [ ] Python已安装（3.8+）
- [ ] 项目文件已解压
- [ ] 成功运行install.bat或start.sh
- [ ] 虚拟环境已创建（venv文件夹）
- [ ] 依赖已安装
- [ ] config.json已创建
- [ ] API Key已填入config.json
- [ ] 后端成功启动（黑窗口显示"Application startup complete"）
- [ ] 前端网页已打开
- [ ] 能点击"获取今日文章"成功获取
- [ ] 能成功进行AI分析

全部打勾 → 安装成功！🎉

---

**祝你学习愉快！有问题随时查看文档。** 🚀

打印版本号：v1.0 | 更新日期：2026-06-06
