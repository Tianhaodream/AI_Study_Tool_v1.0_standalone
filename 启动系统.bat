@echo off
echo 正在启动 AI 评论深度训练系统...
echo 请勿关闭此窗口，系统运行中...

:: 1. 进入后端文件夹并启动后端（后台运行）
start /b cmd /c "cd /d D:\AI_Study_Tool\backend && uvicorn main:app --host 127.0.0.1 --port 8000"

:: 2. 等待 2 秒确保后端启动完成
timeout /t 2 /nobreak >nul

:: 3. 自动打开前端网页
start "" "D:\AI_Study_Tool\frontend\index.html"

echo.
echo 系统已就绪！网页已在浏览器弹出。
echo 如果不想用了，直接关闭这个黑窗口即可。
pause