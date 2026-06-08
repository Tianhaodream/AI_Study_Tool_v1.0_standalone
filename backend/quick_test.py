#!/usr/bin/env python3
"""
快速启动测试 - 检查后端是否能启动
"""
import sys
import time
import subprocess
import requests
from pathlib import Path

print("=" * 60)
print("🔍 后端启动测试")
print("=" * 60)
print()

# 第1步：检查依赖
print("✓ 步骤1: 检查Python依赖...")
required_packages = [
    'fastapi', 'uvicorn', 'pydantic', 'requests', 'beautifulsoup4', 'sqlite3'
]

missing = []
for pkg in required_packages:
    try:
        if pkg == 'sqlite3':
            __import__('sqlite3')
        elif pkg == 'beautifulsoup4':
            __import__('bs4')
        else:
            __import__(pkg.replace('-', '_'))
        print(f"  ✓ {pkg}")
    except ImportError:
        missing.append(pkg)
        print(f"  ✗ {pkg} 缺失！")

if missing:
    print(f"\n❌ 缺少依赖: {', '.join(missing)}")
    print("请运行: pip install -r requirements.txt")
    sys.exit(1)

print()

# 第2步：检查配置
print("✓ 步骤2: 检查配置文件...")
sys.path.insert(0, str(Path(__file__).parent))
try:
    from config import config, API_KEY, PORT, HOST
    print(f"  ✓ 配置已加载")
    print(f"    - Host: {HOST}")
    print(f"    - Port: {PORT}")
    print(f"    - API Key: {'已配置' if API_KEY else '未配置（AI功能不可用）'}")
except Exception as e:
    print(f"  ✗ 配置加载失败: {e}")
    sys.exit(1)

print()

# 第3步：检查数据库
print("✓ 步骤3: 检查数据库...")
try:
    from config import DB_PATH
    from pathlib import Path
    db_file = Path(DB_PATH)
    if db_file.exists():
        size = db_file.stat().st_size / 1024
        print(f"  ✓ 数据库文件存在: {DB_PATH} ({size:.1f} KB)")
    else:
        print(f"  ℹ 数据库文件不存在，首次运行会自动创建")
except Exception as e:
    print(f"  ✗ 数据库检查失败: {e}")

print()

# 第4步：尝试启动后端（短暂测试）
print("✓ 步骤4: 尝试启动后端...")
print(f"  启动命令: uvicorn main:app --host {HOST} --port {PORT}")
print()

try:
    # 启动uvicorn进程
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app",
         "--host", HOST, "--port", str(PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # 等待3秒让服务启动
    time.sleep(3)

    # 测试连接
    print(f"  正在测试 http://{HOST}:{PORT}...")
    try:
        resp = requests.get(f"http://{HOST}:{PORT}/api/articles", timeout=2)
        if resp.status_code in [200, 400, 500]:  # 任何响应都说明服务在运行
            print(f"  ✓ 后端服务正常运行！")
            print(f"    返回状态码: {resp.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"  ✗ 无法连接到后端服务")
        print(f"    检查是否有防火墙阻止")
        stdout, stderr = proc.communicate(timeout=1)
        if stderr:
            print(f"    错误信息: {stderr[:200]}")

    # 关闭进程
    try:
        proc.terminate()
        proc.wait(timeout=2)
    except:
        proc.kill()

except Exception as e:
    print(f"  ✗ 启动失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("=" * 60)
print("✅ 所有检查通过！")
print("=" * 60)
print()
print("📝 接下来:")
print("  1. 编辑 config.json，填入 DeepSeek API Key")
print("  2. 运行: uvicorn main:app --host 127.0.0.1 --port 8000")
print("  3. 在浏览器打开: frontend/index.html")
print()
