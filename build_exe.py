#!/usr/bin/env python3
"""
PyInstaller 构建脚本
将FastAPI后端打包成独立的Windows/Mac/Linux可执行文件
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path
from datetime import datetime


class BuildConfig:
    """构建配置"""
    PROJECT_NAME = "AI-Study-Tool"
    VERSION = "1.0"
    BUILD_DATE = datetime.now().strftime("%Y%m%d")

    # 输出目录
    BUILD_DIR = Path("build")
    DIST_DIR = Path("dist")
    STANDALONE_DIR = DIST_DIR / "standalone"

    # 平台信息
    PLATFORM = platform.system()  # Windows, Darwin (Mac), Linux
    ARCH = platform.machine()  # x86_64, arm64等

    # 输出文件名
    if PLATFORM == "Windows":
        BACKEND_NAME = "ai-study-tool-backend.exe"
        ZIP_NAME = f"{PROJECT_NAME}-v{VERSION}-standalone-{BUILD_DATE}-win64.zip"
    elif PLATFORM == "Darwin":
        BACKEND_NAME = "ai-study-tool-backend"
        ZIP_NAME = f"{PROJECT_NAME}-v{VERSION}-standalone-{BUILD_DATE}-macos.zip"
    else:  # Linux
        BACKEND_NAME = "ai-study-tool-backend"
        ZIP_NAME = f"{PROJECT_NAME}-v{VERSION}-standalone-{BUILD_DATE}-linux.zip"


def check_dependencies():
    """检查必需的依赖"""
    print("检查依赖...")

    required = ["pyinstaller"]

    for package in required:
        try:
            __import__(package)
            print(f"  ✓ {package} 已安装")
        except ImportError:
            print(f"  ✗ {package} 未安装")
            print(f"    运行: pip install {package}")
            return False

    return True


def clean_old_builds():
    """清理旧的构建文件"""
    print("\n清理旧的构建文件...")

    for directory in [BuildConfig.BUILD_DIR, BuildConfig.DIST_DIR]:
        if directory.exists():
            try:
                shutil.rmtree(directory)
                print(f"  ✓ 已删除 {directory}")
            except Exception as e:
                print(f"  ⚠ 无法删除 {directory}: {e}")


def build_backend():
    """使用PyInstaller打包后端"""
    print("\n构建后端可执行文件...")

    # PyInstaller命令
    cmd = [
        "pyinstaller",
        "--onefile",  # 生成单个exe文件
        "--windowed" if BuildConfig.PLATFORM == "Darwin" else "",  # Mac需要
        "--name", "ai-study-tool-backend",
        "--distpath", str(BuildConfig.STANDALONE_DIR),
        "--buildpath", str(BuildConfig.BUILD_DIR),
        "--specpath", ".",
        "--add-data", f"backend/config_template.json{os.pathsep}backend",
        "--hidden-import=fastapi",
        "--hidden-import=uvicorn",
        "--hidden-import=pydantic",
        "--hidden-import=requests",
        "--hidden-import=beautifulsoup4",
        "--hidden-import=sqlite3",
        "backend/main.py"
    ]

    # 移除空字符串
    cmd = [c for c in cmd if c]

    print(f"  运行命令: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, check=True)
        if result.returncode != 0:
            print(f"  ✗ PyInstaller 构建失败")
            return False

        print("  ✓ 后端可执行文件构建成功")
        return True
    except Exception as e:
        print(f"  ✗ 构建出错: {e}")
        return False


def create_launcher_script():
    """创建启动脚本"""
    print("\n创建启动脚本...")

    launcher_content = {
        "Windows": """@echo off
setlocal enabledelayedexpansion

echo.
echo ========================================
echo   AI 评论深度训练系统 - 独立版启动
echo ========================================
echo.

REM 获取脚本所在目录
set SCRIPT_DIR=%~dp0

REM 启动后端服务
echo 启动后端服务...
start "" "%SCRIPT_DIR%ai-study-tool-backend.exe"

REM 等待后端启动
echo 等待后端启动...
timeout /t 3 /nobreak >nul

REM 尝试打开前端网页（支持当前目录或子目录中的frontend）
echo 打开前端网页...
if exist "%SCRIPT_DIR%frontend\\index.html" (
    start "" "%SCRIPT_DIR%frontend\\index.html"
) else if exist "%SCRIPT_DIR%..\\frontend\\index.html" (
    start "" "%SCRIPT_DIR%..\\frontend\\index.html"
) else (
    echo. 
    echo ⚠ 警告：未找到前端文件 frontend/index.html
    echo 请确保前端文件存在或手动打开前端界面
)

echo.
echo ========================================
echo 系统已启动！
echo 后端运行于: http://127.0.0.1:8000
echo 配置文件: config.json (首次运行会自动创建)
echo ========================================
echo.
pause
""",
        "Darwin": """#!/bin/bash

echo ""
echo "========================================"
echo "  AI 评论深度训练系统 - 独立版启动"
echo "========================================"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 启动后端服务
echo "启动后端服务..."
"$SCRIPT_DIR/ai-study-tool-backend" &
BACKEND_PID=$!

# 等待后端启动
echo "等待后端启动..."
sleep 3

# 打开前端网页（支持当前目录或上级目录）
echo "打开前端网页..."
if [ -f "$SCRIPT_DIR/frontend/index.html" ]; then
    open "$SCRIPT_DIR/frontend/index.html"
elif [ -f "$SCRIPT_DIR/../frontend/index.html" ]; then
    open "$SCRIPT_DIR/../frontend/index.html"
else
    echo ""
    echo "⚠ 警告：未找到前端文件 frontend/index.html"
    echo "请确保前端文件存在或手动打开前端界面"
fi

echo ""
echo "========================================"
echo "系统已启动！"
echo "后端运行于: http://127.0.0.1:8000"
echo "配置文件: config.json (首次运行会自动创建)"
echo "========================================"
echo ""

# 等待后端进程
wait $BACKEND_PID
""",
        "Linux": """#!/bin/bash

echo ""
echo "========================================"
echo "  AI 评论深度训练系统 - 独立版启动"
echo "========================================"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 启动后端服务
echo "启动后端服务..."
"$SCRIPT_DIR/ai-study-tool-backend" &
BACKEND_PID=$!

# 等待后端启动
echo "等待后端启动..."
sleep 3

# 打开前端网页（支持当前目录或上级目录）
echo "打开前端网页..."
if [ -f "$SCRIPT_DIR/frontend/index.html" ]; then
    if command -v xdg-open &> /dev/null; then
        xdg-open "$SCRIPT_DIR/frontend/index.html"
    fi
elif [ -f "$SCRIPT_DIR/../frontend/index.html" ]; then
    if command -v xdg-open &> /dev/null; then
        xdg-open "$SCRIPT_DIR/../frontend/index.html"
    fi
else
    echo ""
    echo "⚠ 警告：未找到前端文件 frontend/index.html"
    echo "请确保前端文件存在或手动打开前端界面"
fi

echo ""
echo "========================================"
echo "系统已启动！"
echo "后端运行于: http://127.0.0.1:8000"
echo "配置文件: config.json (首次运行会自动创建)"
echo "========================================"
echo ""

# 等待后端进程
wait $BACKEND_PID
"""
    }

    # 根据平台选择内容
    if BuildConfig.PLATFORM == "Windows":
        script_name = "start.bat"
        content = launcher_content["Windows"]
    else:
        script_name = "start.sh"
        content = launcher_content.get(
            BuildConfig.PLATFORM, launcher_content["Linux"])

    script_path = BuildConfig.STANDALONE_DIR / script_name

    # 确保目录存在
    script_path.parent.mkdir(parents=True, exist_ok=True)

    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(content)

    # Unix系统需要设置执行权限
    if BuildConfig.PLATFORM != "Windows":
        os.chmod(script_path, 0o755)

    print(f"  ✓ 启动脚本已创建: {script_path}")


def copy_frontend():
    """复制前端文件"""
    print("\n复制前端文件...")

    frontend_src = Path("frontend")
    frontend_dst = BuildConfig.STANDALONE_DIR / "frontend"

    if frontend_src.exists():
        # 删除旧的frontend目录
        if frontend_dst.exists():
            shutil.rmtree(frontend_dst)

        # 复制前端文件
        shutil.copytree(frontend_src, frontend_dst)
        print(f"  ✓ 前端文件已复制到 {frontend_dst}")
    else:
        print(f"  ✗ 前端目录不存在: {frontend_src}")
        return False

    return True


def copy_config_template():
    """复制配置文件模板"""
    print("\n复制配置文件...")

    config_files = [
        "backend/config_template.json",
    ]

    for config_file in config_files:
        src = Path(config_file)
        dst = BuildConfig.STANDALONE_DIR / src.name

        if src.exists():
            shutil.copy(src, dst)
            print(f"  ✓ 已复制 {src.name}")
        else:
            print(f"  ⚠ 配置文件不存在: {src}")

    return True


def copy_documentation():
    """复制文档文件"""
    print("\n复制文档文件...")

    doc_files = [
        "README.md",
        "QUICK_START.md",
        "INSTALLATION.md",
        "INSTALL_QUICK_REFERENCE.md",
        "CHANGELOG.md",
    ]

    for doc_file in doc_files:
        src = Path(doc_file)
        dst = BuildConfig.STANDALONE_DIR / src.name

        if src.exists():
            shutil.copy(src, dst)
            print(f"  ✓ 已复制 {doc_file}")

    return True


def create_standalone_package():
    """创建独立exe发布包"""
    print("\n创建独立exe发布包...")

    # 检查standalone目录
    if not BuildConfig.STANDALONE_DIR.exists():
        print(f"  ✗ standalone目录不存在: {BuildConfig.STANDALONE_DIR}")
        return False

    # 创建zip
    releases_dir = Path("releases")
    releases_dir.mkdir(exist_ok=True)

    zip_path = releases_dir / BuildConfig.ZIP_NAME

    # 如果已存在，备份
    if zip_path.exists():
        backup_path = releases_dir / f"{BuildConfig.ZIP_NAME}.bak"
        shutil.copy(zip_path, backup_path)
        print(f"  ⚠ 已存在同名文件，备份为: {backup_path}")

    print(f"  压缩文件: {BuildConfig.ZIP_NAME}")

    try:
        shutil.make_archive(
            str(zip_path.with_suffix("")),  # 去掉.zip后缀
            "zip",
            BuildConfig.STANDALONE_DIR
        )

        zip_size = zip_path.stat().st_size / (1024 * 1024)
        print(f"  ✓ 包已创建: {zip_path}")
        print(f"  ✓ 文件大小: {zip_size:.2f} MB")

        return True
    except Exception as e:
        print(f"  ✗ 打包失败: {e}")
        return False


def create_installer_info():
    """创建安装说明"""
    print("\n创建安装说明...")

    info_content = f"""# AI评论深度训练系统 - 独立版 (v{BuildConfig.VERSION})

## 平台: {BuildConfig.PLATFORM} {BuildConfig.ARCH}

### 特点

✅ 无需安装Python
✅ 完全独立运行
✅ 开箱即用

### 快速开始

#### Windows 用户
1. 解压zip文件
2. 双击 `start.bat`
3. 系统自动启动
4. 编辑 `config_template.json` 填入 API Key

#### Mac/Linux 用户
1. 解压zip文件
2. 运行 `bash start.sh`
3. 系统自动启动
4. 编辑 `config_template.json` 填入 API Key

### 文件说明

- `ai-study-tool-backend.exe` (Windows) / `ai-study-tool-backend` (Mac/Linux)
  后端可执行程序

- `start.bat` / `start.sh`
  启动脚本（自动启动后端和前端）

- `frontend/`
  Web前端界面

- `config_template.json`
  配置文件模板（复制为config.json并填入API Key）

- 文档文件
  README.md, QUICK_START.md, INSTALLATION.md等

### 系统要求

- Windows 7+ / Mac OS 10.14+ / Linux (Ubuntu 18.04+)
- 不需要安装Python
- 网络连接（用于爬虫和AI分析）

### 故障排查

如遇到问题，查看：
- README.md
- INSTALLATION.md
- QUICK_START.md

### 更新日期

{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

    info_path = BuildConfig.STANDALONE_DIR / "README_STANDALONE.md"

    with open(info_path, 'w', encoding='utf-8') as f:
        f.write(info_content)

    print(f"  ✓ 安装说明已创建: README_STANDALONE.md")


def print_summary():
    """打印总结"""
    print("\n" + "=" * 60)
    print("✅ 构建完成！")
    print("=" * 60)
    print()
    print(f"平台: {BuildConfig.PLATFORM} {BuildConfig.ARCH}")
    print(f"发布包: releases/{BuildConfig.ZIP_NAME}")
    print()

    if (Path("releases") / BuildConfig.ZIP_NAME).exists():
        zip_size = (Path("releases") /
                    BuildConfig.ZIP_NAME).stat().st_size / (1024 * 1024)
        print(f"文件大小: {zip_size:.2f} MB")

    print()
    print("下一步:")
    print("1. 下载发布包")
    print("2. 解压到用户电脑")
    print("3. 双击start脚本启动")
    print("4. 无需安装Python环境")
    print()


def main():
    """主构建函数"""
    print()
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║     🔨 PyInstaller 独立exe构建脚本                           ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print()

    # 检查依赖
    if not check_dependencies():
        print("\n请先安装 PyInstaller:")
        print("  pip install pyinstaller")
        return 1

    # 清理旧构建
    clean_old_builds()

    # 构建后端
    if not build_backend():
        print("\n❌ 后端构建失败")
        return 1

    # 创建启动脚本
    create_launcher_script()

    # 复制前端
    if not copy_frontend():
        print("\n❌ 前端文件复制失败")
        return 1

    # 复制配置文件
    copy_config_template()

    # 复制文档
    copy_documentation()

    # 创建安装说明
    create_installer_info()

    # 创建发布包
    if not create_standalone_package():
        print("\n❌ 发布包创建失败")
        return 1

    # 打印总结
    print_summary()

    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n❌ 构建出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
