import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bot.db")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    
    # XP settings
    BASE_XP_RATE = 10
    STREAK_MULTIPLIER = 1.1
    
    # Learning settings
    DAILY_LESSON_LIMIT_FREE = 5
    DAILY_LESSON_LIMIT_PREMIUM = 50
