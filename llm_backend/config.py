import os
from dotenv import load_dotenv
from pathlib import Path

# 自动加载项目根目录的 .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def env(key: str, default=None):
    return os.getenv(key, default)
