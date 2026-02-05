import os
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

# Token .env dan olish
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
DATABASE_PATH = os.getenv("DATABASE_PATH", "./nikoh_bot.db")

# Token borligini tekshirish
if not BOT_TOKEN:
    print("❌ XATOLIK: .env faylida BOT_TOKEN topilmadi!")
    print("✅ .env fayliga quyidagini qo'ying:")
    print("BOT_TOKEN=8219884908:AAHMBf0JP1Cd_w2aGlN_cl_CZmyGoV1gAK4")
else:
    print(f"✅ Token yuklandi: {BOT_TOKEN[:15]}...")
