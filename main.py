import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from database import Database
from handlers import routers
from handlers.admin import router as admin_router  # <- BU QATORNI QO'SHING

# ... qolgan kodlar ...

# Log qilishni sozlash
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def main():
    # Bot va dispatcher yaratish
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Database yaratish
    db = Database()
    await db.init_db()
    
    # Routerlarni ulash
    for router in routers:
        dp.include_router(router)
    
    # Botni ishga tushirish
    logger.info("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
