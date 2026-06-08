"""
配置管理模块
支持从环境变量和配置文件读取配置
首次运行自动初始化配置文件
"""

import os
import json
from pathlib import Path

# 获取当前目录
BASE_DIR = Path(__file__).parent


def _create_default_config():
    """创建默认配置"""
    return {
        "host": "127.0.0.1",
        "port": 8000,
        "db_path": "app.db",
        "api_key": "",  # 空表示需要用户提供
        "crawl_sources": [
            "http://opinion.people.com.cn/GB/436867/index.html",
            "http://opinion.people.com.cn/GB/8213/49160/49219/index.html"
        ],
        "review_days": [1, 2, 4, 7, 15],
        "cors_origins": ["*"],
        "timeout": 10,
        "deepseek_api_url": "https://api.deepseek.com/v1/chat/completions",
        "deepseek_model": "deepseek-chat"
    }


def _auto_init_config():
    """首次运行时自动初始化config.json"""
    config_file = BASE_DIR / "config.json"
    template_file = BASE_DIR / "config_template.json"

    if not config_file.exists():
        default_config = _create_default_config()

        # 尝试从模板文件读取
        if template_file.exists():
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    template_config = json.load(f)
                    default_config.update(template_config)
            except json.JSONDecodeError:
                pass

        # 写入config.json
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            print(f"✓ 首次运行：已自动创建配置文件 {config_file.name}")
            print(f"  请编辑配置文件并填入你的 DeepSeek API Key")
        except Exception as e:
            print(f"⚠ 创建配置文件失败: {e}")


def load_config():
    """
    加载配置文件
    优先级：环境变量 > config.json > 默认值
    首次运行自动初始化config.json
    """

    # 首次运行时自动初始化
    _auto_init_config()

    # 默认配置
    config = _create_default_config()

    # 尝试从环境变量读取
    if os.getenv("DEEPSEEK_API_KEY"):
        config["api_key"] = os.getenv("DEEPSEEK_API_KEY")

    # 尝试从config.json读取
    config_file = BASE_DIR / "config.json"
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                config.update(user_config)
                print(f"✓ 已从 {config_file.name} 加载配置")
        except json.JSONDecodeError as e:
            print(f"⚠ 配置文件格式错误: {e}，使用默认配置")

    # 验证API Key
    if not config["api_key"]:
        print("\n⚠️  警告：未配置 DeepSeek API Key！")
        print("   AI分析功能将无法使用")
        print("   请编辑 config.json 并填入 'api_key' 字段")
        print("   获取API Key: https://platform.deepseek.com/")

    return config


# 加载配置
config = load_config()

# 导出常用配置
DB_PATH = config.get("db_path", "app.db")
API_KEY = config.get("api_key", "")
HOST = config.get("host", "127.0.0.1")
PORT = config.get("port", 8000)
CRAWL_SOURCES = config.get("crawl_sources", [])
REVIEW_DAYS = config.get("review_days", [1, 2, 4, 7, 15])
CORS_ORIGINS = config.get("cors_origins", ["*"])
TIMEOUT = config.get("timeout", 10)
DEEPSEEK_API_URL = config.get(
    "deepseek_api_url", "https://api.deepseek.com/v1/chat/completions")
DEEPSEEK_MODEL = config.get("deepseek_model", "deepseek-chat")
