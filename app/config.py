"""应用配置：从环境变量 / .env 读取 DeepSeek 接入参数。"""
import os

from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")


def require_api_key() -> str:
    if not DEEPSEEK_API_KEY:
        raise RuntimeError(
            "未配置 DEEPSEEK_API_KEY。请复制 .env.example 为 .env 并填入密钥，"
            "或设置同名环境变量。"
        )
    return DEEPSEEK_API_KEY
