#!/bin/bash

# AI 评论深度训练系统 - 启动脚本（Mac/Linux）

echo "========================================"
echo "  AI 评论深度训练系统 - 启动向导"
echo "========================================"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未检测到Python3安装"
    echo "请先从 https://www.python.org 下载并安装Python 3.8+"
    exit 1
fi

python3 --version
echo "✓ Python已安装"
echo ""

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境中..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ 虚拟环境创建失败"
        exit 1
    fi
    echo "✓ 虚拟环境创建成功"
fi

# 激活虚拟环境
source venv/bin/activate
echo "✓ 虚拟环境已激活"
echo ""

# 安装依赖
echo "📚 检查并安装依赖包..."
pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi
echo "✓ 依赖安装成功"
echo ""

# 检查配置文件
if [ ! -f "config.json" ]; then
    echo "⚠️  未找到config.json文件"
    echo "正在从config_template.json创建..."
    cp config_template.json config.json
    echo "✓ config.json已创建"
    echo ""
    echo "📝 请编辑 config.json 并填入你的DeepSeek API Key"
    echo "    之后重新运行此脚本"
    echo ""
    exit 0
fi

# 启动后端
echo "🚀 启动后端服务..."
uvicorn main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

# 等待后端启动
echo "⏳ 等待后端启动（3秒）..."
sleep 3

# 打开前端
echo "🌐 打开浏览器..."
if command -v open &> /dev/null; then
    open "../frontend/index.html"
elif command -v xdg-open &> /dev/null; then
    xdg-open "../frontend/index.html"
fi

echo ""
echo "========================================"
echo "✅ 系统已启动！"
echo ""
echo "📖 使用提示："
echo "  - 后端API：http://127.0.0.1:8000"
echo "  - 配置文件：$(pwd)/config.json"
echo "  - 数据库：$(pwd)/app.db"
echo ""
echo "🛑 关闭后端：按 Ctrl+C"
echo "========================================"
echo ""

wait $BACKEND_PID
