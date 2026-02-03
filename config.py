import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
DATABASE_PATH = os.getenv("DATABASE_PATH", "./nikoh_bot.db")

# Kurslar
USD_TO_UZS = 12100
RUB_TO_UZS = 140

# Bonuslar
BONUS_300K = 0.10  # 10%
BONUS_500K = 0.15  # 15%
BONUS_1M = 0.20    # 20%

# To'lov minimal summasi
MIN_USD = 4
MIN_UZS = 50000
MIN_RUB = 5000
MIN_TRY = 500
