@echo off
REM AI 学习工具 - GitHub 一键配置上传脚本
REM 用途：快速配置 Git 远程并创建 Release

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║    AI 学习工具 - GitHub 上传配置助手                      ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM 检查 Git 是否安装
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git 未安装！请先安装 Git: https://git-scm.com/download/win
    pause
    exit /b 1
)
echo ✅ Git 已安装

REM 询问 GitHub 仓库地址
echo.
echo 📝 请输入你的 GitHub 仓库地址（例如：https://github.com/username/AI_Study_Tool）
set /p REPO_URL="仓库地址: "

if "!REPO_URL!"=="" (
    echo ❌ 仓库地址不能为空
    pause
    exit /b 1
)

REM 检查是否已有远程配置
cd /d %~dp0..
git remote -v >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Git 已配置
    for /f "tokens=2" %%i in ('git remote -v ^| findstr origin ^| findstr fetch') do (
        echo 当前远程: %%i
        set EXISTING_REMOTE=%%i
    )
) else (
    echo ℹ️  未配置 Git 远程
)

echo.
echo 🔧 配置选项:
echo.
echo 1. 添加 Git 远程（如果还没有）
echo 2. 更新 Git 远程（覆盖现有配置）
echo 3. 只查看当前配置（不修改）
echo.
set /p CHOICE="请选择 (1/2/3): "

if "!CHOICE!"=="1" (
    git remote add origin !REPO_URL!
    echo ✅ Git 远程已添加
) else if "!CHOICE!"=="2" (
    git remote remove origin
    git remote add origin !REPO_URL!
    echo ✅ Git 远程已更新
) else if "!CHOICE!"=="3" (
    echo 当前配置:
    git remote -v
) else (
    echo ❌ 无效选择
    exit /b 1
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 📋 下一步操作建议：
echo.
echo 【方式 1 - 使用网页界面（推荐）】
echo   1. 访问: !REPO_URL!/releases
echo   2. 点击 "Draft a new release"
echo   3. 设置版本号: v1.0
echo   4. 添加发布说明（参考 GITHUB_UPLOAD_GUIDE.md）
echo   5. 上传文件:
echo      - AI-Study-Tool-v1.0-source-20260608.zip
echo      - AI-Study-Tool-v1.0-standalone-20260608-win64.zip
echo   6. 点击 "Publish release"
echo.
echo 【方式 2 - 使用命令行】
echo   运行以下命令:
echo.
echo   cd D:\AI_Study_Tool
echo   git add .
echo   git commit -m "release: v1.0 发布"
echo   git push -u origin main
echo.
echo   然后在 GitHub 网页创建 Release（参考方式 1）
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 📖 详细指南已保存到: releases\GITHUB_UPLOAD_GUIDE.md
echo.
echo 需要帮助？打开上面的文件查看详细说明。
echo.

pause
