import os
from dotenv import load_dotenv

load_dotenv()

# Bot tokeni
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi! .env faylini tekshiring.")

# Admin ID
ADMIN_ID = os.getenv("ADMIN_ID", "")

# Database URL (PostgreSQL)
DATABASE_URL = os.getenv("DATABASE_URL")

# Kurslar va bonuslar
USD_TO_UZS = 12100
BONUS_300K = 0.10
BONUS_500K = 0.15
BONUS_1M = 0.20

# Minimal to'lovlar
MIN_USD = 4
MIN_UZS = 50000

print(f"✅ Config yuklandi. Bot tokeni: {BOT_TOKEN[:15]}...")