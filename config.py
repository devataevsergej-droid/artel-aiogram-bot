import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMIN_ID = int(os.getenv("ADMIN_ID", 558864284))
    ADMIN_GROUP_ID = int(os.getenv("ADMIN_GROUP_ID", -1003894573982))
    CHAT_GROUP_ID = int(os.getenv("CHAT_GROUP_ID", -1002324866523))
    CHANNEL_URL = os.getenv("CHANNEL_URL", "https://t.me/artelena_test")
    CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "artelena_test")
    MASTER_USERNAME = os.getenv("MASTER_USERNAME", "YelenaFelix")
    BOT_USERNAME = os.getenv("BOT_USERNAME", "ArtEl_LSK_bot")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    
    RANKS = [
        {"name": "Новичок", "min_score": 0, "discount": 5},
        {"name": "Путник", "min_score": 500, "discount": 6},
        {"name": "Искатель", "min_score": 1000, "discount": 7},
        {"name": "Знаток", "min_score": 2000, "discount": 8},
        {"name": "Мастер", "min_score": 4000, "discount": 10},
        {"name": "Профи", "min_score": 7000, "discount": 12},
        {"name": "Легенда", "min_score": 10000, "discount": 15}
    ]

config = Config()