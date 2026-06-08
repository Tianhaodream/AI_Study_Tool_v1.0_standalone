#!/usr/bin/env python3
"""
自动打包脚本 - 生成轻量化的发布包
用途：将项目打包成zip文件，准备分发给用户
"""

import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

# 项目信息
PROJECT_NAME = "AI-Study-Tool"
VERSION = "1.0"
RELEASE_DATE = datetime.now().strftime("%Y%m%d")

# 定义需要打包的文件和目录
INCLUDE_DIRS = [
    "backend",
    "frontend",
]

INCLUDE_FILES = [
    "README.md",
    "QUICK_START.md",
    "INSTALLATION.md",
    ".gitignore",
    "setup.py",
]

# 需要排除的目录和文件
EXCLUDE_DIRS = {
    "__pycache__",
    ".git",
    ".vscode",
    ".idea",
    "venv",
    "env",
    "node_modules",
}

EXCLUDE_FILES = {
    "*.pyc",
    "*.pyo",
    ".DS_Store",
    "app.db",
    "config.json",
    ".env",
}


def should_exclude(path):
    """检查文件或目录是否应该被排除"""
    name = Path(path).name

    # 检查目录名
    if name in EXCLUDE_DIRS:
        return True

    # 检查文件名
    for pattern in EXCLUDE_FILES:
        if pattern.startswith("*"):
            ext = pattern[1:]
            if Path(path).suffix == ext:
                return True
        elif name == pattern:
            return True

    return False


def create_release_zip():
    """创建发布包"""

    # 创建releases目录
    releases_dir = Path("releases")
    releases_dir.mkdir(exist_ok=True)

    # 生成zip文件名
    zip_name = f"{PROJECT_NAME}-v{VERSION}-{RELEASE_DATE}.zip"
    zip_path = releases_dir / zip_name

    # 如果已存在，创建备份
    if zip_path.exists():
        backup_path = releases_dir / f"{zip_name}.bak"
        shutil.copy(zip_path, backup_path)
        print(f"⚠️  已存在同名文件，备份为: {backup_path}")

    print(f"📦 正在创建发布包: {zip_name}")
    print(f"   目标路径: {zip_path.absolute()}")
    print()

    # 创建zip文件
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:

        # 添加目录
        for dir_name in INCLUDE_DIRS:
            dir_path = Path(dir_name)
            if dir_path.exists():
                print(f"  📁 添加目录: {dir_name}/")
                for root, dirs, files in os.walk(dir_path):
                    # 过滤需要排除的子目录
                    dirs[:] = [d for d in dirs if not should_exclude(d)]

                    for file in files:
                        file_path = Path(root) / file

                        # 跳过需要排除的文件
                        if should_exclude(file_path):
                            continue

                        # 相对路径用于zip中的位置
                        arcname = file_path.relative_to('.')
                        zipf.write(file_path, arcname)
                        print(f"      ✓ {arcname}")

        # 添加文件
        for file_name in INCLUDE_FILES:
            file_path = Path(file_name)
            if file_path.exists():
                print(f"  📄 添加文件: {file_name}")
                zipf.write(file_path, file_name)

    # 获取文件大小
    zip_size = zip_path.stat().st_size / (1024 * 1024)  # 转换为MB

    print()
    print("=" * 60)
    print("✅ 打包成功！")
    print("=" * 60)
    print(f"📦 文件名: {zip_name}")
    print(f"📊 文件大小: {zip_size:.2f} MB")
    print(f"📍 保存位置: {zip_path.absolute()}")
    print()

    return zip_path


def create_releases_readme():
    """创建releases目录下的README"""

    releases_readme = Path("releases") / "README.md"

    content = f"""# 📦 发布包

## 最新版本

**版本**: {VERSION}
**发布日期**: {datetime.now().strftime("%Y年%m月%d日")}

### 下载链接

- `AI-Study-Tool-v{VERSION}-*.zip` - 轻量化包（推荐）

## 包内容

```
AI-Study-Tool/
├── backend/                    # 后端服务
│   ├── main.py                # FastAPI应用
│   ├── config.py              # 配置管理
│   ├── config_template.json   # 配置模板
│   ├── install.bat            # Windows启动脚本
│   ├── start.sh               # Mac/Linux启动脚本
│   └── requirements.txt        # 依赖列表
├── frontend/
│   └── index.html             # 前端界面
├── README.md                  # 项目说明
├── QUICK_START.md             # 快速开始（5分钟）
├── INSTALLATION.md            # 完整安装指南
├── setup.py                   # 打包配置
└── .gitignore                 # Git配置
```

## 快速开始

### Windows
```bash
cd backend
install.bat
```

### Mac/Linux
```bash
cd backend
bash start.sh
```

## 系统要求

- Python 3.8+
- 网络连接
- 100MB磁盘空间

## 详细文档

- 📖 [完整项目文档](../README.md)
- ⚡ [5分钟快速开始](../QUICK_START.md)
- 📋 [完整安装指南](../INSTALLATION.md)

## 版本历史

### v{VERSION} ({datetime.now().strftime("%Y-%m-%d")})
- ✨ 首次发布
- ✅ 一键安装和启动
- ✅ API Key自动记住
- ✅ 跨平台支持
- ✅ 详细文档

## 反馈与支持

遇到问题？
1. 查看 INSTALLATION.md 中的常见问题
2. 检查后端黑窗口的错误信息
3. 查看 README.md 故障排查章节

---

**祝你使用愉快！🚀**
"""

    with open(releases_readme, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ 已创建 releases/README.md")


def main():
    """主函数"""
    print()
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║     🚀 AI评论训练系统 - 自动打包脚本                          ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print()

    try:
        # 创建发布包
        zip_path = create_release_zip()

        # 创建releases README
        create_releases_readme()

        print()
        print("✨ 所有任务完成！")
        print()
        print("📝 下一步建议：")
        print("   1. 上传zip文件到GitHub Releases")
        print("   2. 分享下载链接给用户")
        print("   3. 收集用户反馈")
        print()

    except Exception as e:
        print(f"❌ 出错：{e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
