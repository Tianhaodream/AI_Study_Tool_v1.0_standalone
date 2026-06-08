from config import load_config
import sys
sys.path.insert(0, '.')

# 测试加载
print("\n=== 测试config自动初始化 ===")
config = load_config()
print(f"\n✓ config已加载")
print(f"  Host: {config['host']}")
print(f"  Port: {config['port']}")
print(f"  DB Path: {config['db_path']}")
print(f"  API Key状态: {'已配置' if config['api_key'] else '未配置（正常）'}")
