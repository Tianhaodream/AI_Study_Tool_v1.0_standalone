@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ========================================
echo   AI 评论深度训练系统 - 启动向导
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未检测到Python安装
    echo 请先从 https://www.python.org 下载并安装Python 3.8+
    echo.
    pause
    exit /b 1
)

echo ✓ Python已安装

REM 检查虚拟环境
if not exist "venv" (
    echo.
    echo 📦 创建虚拟环境中...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ 虚拟环境创建失败
        pause
        exit /b 1
    )
    echo ✓ 虚拟环境创建成功
)

REM 激活虚拟环境
call venv\Scripts\activate.bat
echo ✓ 虚拟环境已激活

REM 检查并安装依赖
echo.
echo 📚 检查并安装依赖包...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)
echo ✓ 依赖安装成功

REM 检查配置文件
if not exist "config.json" (
    echo.
    echo ⚠️  未找到config.json文件
    echo 正在从config_template.json创建...
    copy config_template.json config.json >nul
    echo ✓ config.json已创建
    echo.
    echo 📝 请编辑 config.json 并填入你的DeepSeek API Key
    echo    之后重新运行此脚本
    echo.
    pause
    exit /b 0
)

REM 启动后端
echo.
echo 🚀 启动后端服务...
start cmd /k "cd /d %cd% && venv\Scripts\activate.bat && uvicorn main:app --host 127.0.0.1 --port 8000"

REM 等待后端启动
echo ⏳ 等待后端启动（3秒）...
timeout /t 3 /nobreak >nul

REM 打开前端
echo 🌐 打开浏览器...
start "" "..\frontend\index.html"

echo.
echo ========================================
echo ✅ 系统已启动！
echo.
echo 📖 使用提示：
echo   - 前端网址：%CD%\..\frontend\index.html
echo   - 后端API：http://127.0.0.1:8000
echo   - 配置文件：%CD%\config.json
echo   - 数据库：%CD%\app.db
echo.
echo 🛑 关闭后端：直接关闭黑色终端窗口
echo ========================================
echo.
pause
