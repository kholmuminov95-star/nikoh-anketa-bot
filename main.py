import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from database import Database

# Log qilishni sozlash
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Global bot
bot_instance = None

async def main():
    global bot_instance
    
    # Bot va dispatcher yaratish
    bot_instance = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Database yaratish
    db = Database()
    await db.init_db()
    logger.info("Database initialized")
    
    # =========== IMPORT HANDLERS ===========
    logger.info("Importing handlers...")
    
    # 1. Start handler
    from handlers.start import router as start_router
    dp.include_router(start_router)
    logger.info("Start handler loaded")
    
    # 2. Profile handler
    from handlers.profile import router as profile_router
    dp.include_router(profile_router)
    logger.info("Profile handler loaded")
    
    # 3. Payment handler
    from handlers.payment import router as payment_router
    dp.include_router(payment_router)
    logger.info("Payment handler loaded")
    
    # 4. Request handler
    from handlers.request import router as request_router
    dp.include_router(request_router)
    logger.info("Request handler loaded")
    
    # 5. Admin handler
    from handlers.admin import router as admin_router
    dp.include_router(admin_router)
    logger.info("Admin handler loaded")
    
    # =========== BOTNI ISHGA TUSHIRISH ===========
    
    logger.info("✅ Bot ishga tushdi...")
    
    try:
        await dp.start_polling(bot_instance)
    except Exception as e:
        logger.error(f"Botda xatolik: {e}")
    finally:
        await bot_instance.session.close()

def get_bot():
    return bot_instance

if __name__ == "__main__":
    asyncio.run(main())
