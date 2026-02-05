import os
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

# Bot sozlamalari
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
DATABASE_PATH = os.getenv("DATABASE_PATH", "./nikoh_bot.db")

# Valyuta kurslari
USD_TO_UZS = 12100
RUB_TO_UZS = 140
TRY_TO_UZS = 400

# Bonuslar
BONUS_300K = 0.10  # 10%
BONUS_500K = 0.15  # 15%
BONUS_1M = 0.20    # 20%

# Minimal to'lovlar
MIN_USD = 4
MIN_UZS = 50000
MIN_RUB = 5000
MIN_TRY = 500

# Token borligini tekshirish
if not BOT_TOKEN:
    print("❌ XATOLIK: .env faylida BOT_TOKEN topilmadi!")
    print("✅ .env fayliga quyidagini qo'ying:")
    print("BOT_TOKEN=8219884908:AAHMBf0JP1Cd_w2aGlN_cl_CZmyGoV1gAK4")
else:
    print(f"✅ Token yuklandi: {BOT_TOKEN[:15]}...")
