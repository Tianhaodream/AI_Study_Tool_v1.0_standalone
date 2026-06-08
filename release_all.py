#!/usr/bin/env python3
"""
完整发布脚本 - 一键生成双版本包
1. 源码版（开发者和源码爱好者）
2. 一键版（小白用户，已包含打包的exe）

使用前须知：
  - 确保已运行 build_exe.py 生成了可执行文件
  - 或本脚本会自动尝试运行 build_exe.py
"""

import os
import sys
import subprocess
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

# 项目信息
PROJECT_NAME = "AI-Study-Tool"
VERSION = "1.0"
RELEASE_DATE = datetime.now().strftime("%Y%m%d")

# 打包配置
SOURCE_INCLUDE_DIRS = [
    "backend",
    "frontend",
]

SOURCE_INCLUDE_FILES = [
    "README.md",
    "QUICK_START.md",
    "INSTALLATION.md",
    "INSTALL_QUICK_REFERENCE.md",
    "CHANGELOG.md",
    "setup.py",
    ".gitignore",
]

# 排除配置
EXCLUDE_DIRS = {
    "__pycache__",
    ".git",
    ".vscode",
    ".idea",
    "venv",
    "env",
    "node_modules",
    "build",  # PyInstaller的build目录
    "dist",   # 旧的dist
}

EXCLUDE_FILES = {
    "*.pyc",
    "*.pyo",
    ".DS_Store",
    "app.db",
    "config.json",
    ".env",
    "*.spec",  # PyInstaller生成的spec文件
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


def ensure_standalone_exists():
    """确保standalone目录存在，如不存在则尝试运行build_exe.py"""
    standalone_dir = Path("dist") / "standalone"

    if standalone_dir.exists() and list(standalone_dir.glob("*")):
        print(f"✓ 发现已有的standalone包: {standalone_dir}")
        return True

    print("⚠ 未找到standalone包，尝试构建...")
    try:
        result = subprocess.run(
            [sys.executable, "build_exe.py"],
            check=False,
            capture_output=False
        )
        if result.returncode != 0:
            print("❌ 构建失败，请先运行 build_exe.py")
            return False
        return True
    except Exception as e:
        print(f"❌ 运行build_exe.py失败: {e}")
        return False


def create_source_zip():
    """创建源码版zip（开发者版）"""
    print("\n" + "=" * 60)
    print("📦 创建源码版本...")
    print("=" * 60)

    releases_dir = Path("releases")
    releases_dir.mkdir(exist_ok=True)

    zip_name = f"{PROJECT_NAME}-v{VERSION}-source-{RELEASE_DATE}.zip"
    zip_path = releases_dir / zip_name

    # 备份已存在的文件
    if zip_path.exists():
        backup_path = releases_dir / f"{zip_name}.bak"
        shutil.copy(zip_path, backup_path)
        print(f"⚠ 已存在同名文件，备份为: {backup_path}")

    print(f"正在创建: {zip_name}")

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 添加目录
        for dir_name in SOURCE_INCLUDE_DIRS:
            dir_path = Path(dir_name)
            if dir_path.exists():
                print(f"  📁 添加目录: {dir_name}/")
                for root, dirs, files in os.walk(dir_path):
                    dirs[:] = [d for d in dirs if not should_exclude(d)]

                    for file in files:
                        file_path = Path(root) / file
                        if should_exclude(file_path):
                            continue

                        arcname = file_path.relative_to('.')
                        zipf.write(file_path, arcname)

        # 添加文件
        for file_name in SOURCE_INCLUDE_FILES:
            file_path = Path(file_name)
            if file_path.exists():
                print(f"  📄 添加文件: {file_name}")
                zipf.write(file_path, file_name)

    zip_size = zip_path.stat().st_size / (1024 * 1024)
    print(f"✓ 源码版本完成: {zip_size:.2f} MB")

    return zip_path


def create_standalone_zip():
    """创建一键版zip（小白用户版）"""
    print("\n" + "=" * 60)
    print("🎁 创建一键版本（Windows免Python）...")
    print("=" * 60)

    standalone_dir = Path("dist") / "standalone"

    if not standalone_dir.exists():
        print("❌ standalone目录不存在")
        return None

    releases_dir = Path("releases")
    releases_dir.mkdir(exist_ok=True)

    # 确定系统标识
    import platform
    if platform.system() == "Windows":
        platform_suffix = "win64"
    elif platform.system() == "Darwin":
        platform_suffix = "macos"
    else:
        platform_suffix = "linux"

    zip_name = f"{PROJECT_NAME}-v{VERSION}-standalone-{RELEASE_DATE}-{platform_suffix}.zip"
    zip_path = releases_dir / zip_name

    # 备份已存在的文件
    if zip_path.exists():
        backup_path = releases_dir / f"{zip_name}.bak"
        shutil.copy(zip_path, backup_path)
        print(f"⚠ 已存在同名文件，备份为: {backup_path}")

    print(f"正在创建: {zip_name}")
    print(f"  打包目录: {standalone_dir}")

    # 创建zip
    shutil.make_archive(
        str(zip_path.with_suffix("")),
        "zip",
        standalone_dir
    )

    zip_size = zip_path.stat().st_size / (1024 * 1024)
    print(f"✓ 一键版本完成: {zip_size:.2f} MB")

    return zip_path


def create_releases_readme():
    """创建releases目录下的README"""
    releases_readme = Path("releases") / "README.md"

    content = f"""# 📦 发布包

## 最新版本

**版本**: {VERSION}  
**发布日期**: {datetime.now().strftime("%Y年%m月%d日")}

---

## 📥 选择适合你的版本

### 🎁 一键版（推荐小白用户）

**文件名**: `{PROJECT_NAME}-v{VERSION}-standalone-{RELEASE_DATE}-*.zip`

**特点**:
- ✅ **无需安装Python** - 开箱即用
- ✅ **一键启动** - 双击start.bat/sh启动
- ✅ **轻松上手** - 完全面向小白用户
- ✅ **包含所有依赖** - 无需额外配置

**系统要求**:
- Windows 7+ / Mac OS 10.14+ / Linux
- 不需要安装Python
- 网络连接（用于爬虫和AI分析）

**快速开始**:
1. 解压zip文件
2. 双击 `start.bat` (Windows) 或运行 `bash start.sh` (Mac/Linux)
3. 浏览器自动打开
4. 按提示填入DeepSeek API Key

---

### 👨‍💻 源码版（推荐开发者）

**文件名**: `{PROJECT_NAME}-v{VERSION}-source-{RELEASE_DATE}.zip`

**特点**:
- 完整源代码
- 可以自由修改和扩展
- 适合学习和开发
- 需要手动配置Python环境

**系统要求**:
- Python 3.8+
- pip（Python包管理器）
- 网络连接

**快速开始**:
1. 解压zip文件
2. 进入backend目录：`cd backend`
3. 安装依赖：`pip install -r requirements.txt`
4. 启动系统：`uvicorn main:app --host 127.0.0.1 --port 8000`
5. 打开前端：`frontend/index.html`

---

## 🔑 API Key配置（两个版本都需要）

首次运行后，系统会自动创建 `config.json` 文件。

### 步骤

1. 获取DeepSeek API Key
   - 访问 [DeepSeek官网](https://platform.deepseek.com)
   - 注册账户，创建API Key
   
2. 编辑 `config.json`，填入API Key
   ```json
   "api_key": "sk-你的Key"
   ```
   
3. 保存并重启系统

---

## 📋 包内容对比

| 文件 | 一键版 | 源码版 |
|------|--------|--------|
| 可执行文件(exe/bin) | ✅ | ❌ |
| Python依赖 | ✅（已内置） | ❌（需pip安装） |
| 前端文件 | ✅ | ✅ |
| 源代码 | ❌ | ✅ |
| 文档 | ✅ | ✅ |

---

## 🚀 功能列表

### 核心功能
- ✨ 自动获取人民网评论文章
- 🏷️ 三色标注系统（问题/原因/对策）
- 🤖 AI深度分析（基于DeepSeek）
- 📚 智能复习计划（间隔重复）
- 💾 本地数据永久保存

### 学习工具
- 📊 学习进度统计
- 🎯 个性化复习提醒
- 📝 多维度标注和笔记
- 🔍 全文搜索和快速查找

---

## 🐛 常见问题

### Q: 一键版和源码版有什么区别？
**A**: 
- 一键版面向小白用户，无需安装Python，开箱即用
- 源码版面向开发者，可以修改代码和扩展功能

### Q: 我应该选哪个版本？
**A**:
- 如果只想使用系统 → **选择一键版**
- 如果要修改代码或贡献 → **选择源码版**

### Q: 一键版的exe文件是怎么来的？
**A**: 使用PyInstaller将Python代码打包成可执行文件，这样就无需用户安装Python

### Q: 能否在两个版本之间切换？
**A**: 可以的。它们的数据库和配置是兼容的，可以互相使用

### Q: API Key真的需要吗？
**A**: 只有在使用AI分析功能时才需要。没有API Key也可以使用标注和复习功能

---

## 📖 详细文档

- 📘 [完整项目文档](https://github.com/your-repo/blob/main/README.md)
- ⚡ [5分钟快速开始](https://github.com/your-repo/blob/main/QUICK_START.md)
- 📋 [完整安装指南](https://github.com/your-repo/blob/main/INSTALLATION.md)

---

## 📜 版本历史

### v{VERSION} ({datetime.now().strftime("%Y-%m-%d")})

**新增**:
- ✨ 双版本发布（一键版 + 源码版）
- ✨ 首次运行自动初始化配置
- ✨ 相对路径支持（可随意移动目录）

**改进**:
- 🔧 增强配置加载逻辑
- 🔧 改进启动脚本容错能力
- 📝 优化文档，优先一键版使用说明

**修复**:
- 🐛 修复路径硬编码问题
- 🐛 改善错误提示信息

---

## 🤝 反馈与支持

遇到问题？
1. 查看 QUICK_START.md 中的常见问题
2. 查看后端黑窗口的错误信息
3. 查看 README.md 中的故障排查章节

---

**祝你使用愉快！🚀**

更新时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

    with open(releases_readme, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✓ 已创建 releases/README.md")


def clean_old_builds():
    """清理旧的build/dist目录（仅保留最新）"""
    print("\n" + "=" * 60)
    print("🧹 清理旧的构建产物...")
    print("=" * 60)

    for dir_name in ["build", "dist"]:
        dir_path = Path(dir_name)
        if dir_path.exists():
            try:
                shutil.rmtree(dir_path)
                print(f"✓ 已删除 {dir_name}/")
            except Exception as e:
                print(f"⚠ 无法删除 {dir_name}/: {e}")


def print_summary(source_zip, standalone_zip):
    """打印总结"""
    print("\n" + "=" * 60)
    print("✅ 发布完成！")
    print("=" * 60)
    print()

    if source_zip and source_zip.exists():
        size = source_zip.stat().st_size / (1024 * 1024)
        print(f"📦 源码版本: releases/{source_zip.name}")
        print(f"   大小: {size:.2f} MB")
        print()

    if standalone_zip and standalone_zip.exists():
        size = standalone_zip.stat().st_size / (1024 * 1024)
        print(f"🎁 一键版本: releases/{standalone_zip.name}")
        print(f"   大小: {size:.2f} MB")
        print()

    print("📝 下一步建议：")
    print("   1. 上传zip文件到GitHub Releases")
    print("   2. 分享下载链接给用户")
    print("   3. 收集用户反馈和建议")
    print()


def main():
    """主函数"""
    print()
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║     🚀 AI评论训练系统 - 双版本发布脚本                        ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print()

    try:
        # 确保standalone包存在
        if not ensure_standalone_exists():
            print("\n❌ 无法找到或创建standalone包")
            return 1

        # 创建源码版本
        source_zip = create_source_zip()

        # 创建一键版本
        standalone_zip = create_standalone_zip()

        # 创建releases README
        create_releases_readme()

        # 打印总结
        print_summary(source_zip, standalone_zip)

        print("✨ 所有任务完成！")
        print()

        return 0

    except Exception as e:
        print(f"\n❌ 出错：{e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
