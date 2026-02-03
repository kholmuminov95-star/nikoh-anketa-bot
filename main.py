import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Update
from aiohttp import web

# Log sozlash
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global obyektlar
bot = None
dp = None

async def handle_webhook(request):
    """Telegram webhook requestlarini qabul qilish"""
    try:
        # JSON ma'lumotlarni olish
        data = await request.json()
        
        # Update obyektini yaratish
        update = Update(**data)
        
        # Update ni dispatcherga yuborish
        await dp.feed_update(bot, update)
        
        return web.Response(text="OK")
        
    except Exception as e:
        logger.error(f"Webhook xatosi: {e}")
        return web.Response(text="Error", status=500)

async def health_check(request):
    """Health check endpoint - Railway monitoring uchun"""
    return web.Response(text="✅ Bot ishlayapti!")

async def init_bot():
    """Botni ishga tushirish"""
    global bot, dp
    
    try:
        # Bot tokenini olish
        BOT_TOKEN = os.getenv("BOT_TOKEN")
        if not BOT_TOKEN:
            logger.error("❌ BOT_TOKEN topilmadi!")
            return
        
        # Bot va Dispatcher yaratish
        bot = Bot(token=BOT_TOKEN)
        dp = Dispatcher(storage=MemoryStorage())
        
        logger.info("✅ Bot va Dispatcher yaratildi")
        
        # Database ni ishga tushirish
        from database import Database
        db = Database()
        await db.init_db()
        logger.info("✅ Database ishga tushirildi")
        
        # Handlers ni import qilish va ulash
        logger.info("📥 Handlers yuklanmoqda...")
        
        # Start handler
        try:
            from handlers.start import router as start_router
            dp.include_router(start_router)
            logger.info("✅ Start handler yuklandi")
        except Exception as e:
            logger.error(f"❌ Start handler xatosi: {e}")
        
        # Profile handler
        try:
            from handlers.profile import router as profile_router
            dp.include_router(profile_router)
            logger.info("✅ Profile handler yuklandi")
        except Exception as e:
            logger.error(f"❌ Profile handler xatosi: {e}")
        
        # Payment handler
        try:
            from handlers.payment import router as payment_router
            dp.include_router(payment_router)
            logger.info("✅ Payment handler yuklandi")
        except Exception as e:
            logger.error(f"❌ Payment handler xatosi: {e}")
        
        # Request handler
        try:
            from handlers.request import router as request_router
            dp.include_router(request_router)
            logger.info("✅ Request handler yuklandi")
        except Exception as e:
            logger.error(f"❌ Request handler xatosi: {e}")
        
        # Admin handler
        try:
            from handlers.admin import router as admin_router
            dp.include_router(admin_router)
            logger.info("✅ Admin handler yuklandi")
        except Exception as e:
            logger.error(f"❌ Admin handler xatosi: {e}")
        
        logger.info("🎉 Barcha handlers muvaffaqiyatli yuklandi!")
        
    except Exception as e:
        logger.error(f"❌ Botni ishga tushirishda xatolik: {e}")
        raise

async def on_startup(app):
    """Server ishga tushganda"""
    logger.info("🚀 Server ishga tushmoqda...")
    await init_bot()
    
    # Webhook ni sozlash (agar URL berilgan bo'lsa)
    webhook_url = os.getenv("WEBHOOK_URL")
    if webhook_url and bot:
        try:
            await bot.set_webhook(
                url=webhook_url,
                drop_pending_updates=True
            )
            logger.info(f"🌐 Webhook sozlandi: {webhook_url}")
        except Exception as e:
            logger.error(f"❌ Webhook sozlashda xatolik: {e}")

async def on_shutdown(app):
    """Server to'xtaganda"""
    logger.info("🛑 Server to'xtamoqda...")
    
    if bot:
        # Webhook ni o'chirish
        try:
            await bot.delete_webhook(drop_pending_updates=True)
            logger.info("🌐 Webhook o'chirildi")
        except Exception as e:
            logger.error(f"❌ Webhook o'chirishda xatolik: {e}")
        
        # Session ni yopish
        await bot.session.close()
        logger.info("✅ Session yopildi")

def create_app():
    """Web application yaratish"""
    app = web.Application()
    
    # Route'lar
    app.router.add_post("/webhook", handle_webhook)
    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)
    
    # Startup/shutdown handlerlar
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    
    return app

def main():
    """Asosiy dastur"""
    # Port ni aniqlash
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"🚀 Server {host}:{port} da ishga tushmoqda...")
    
    # App ni ishga tushirish
    app = create_app()
    web.run_app(app, host=host, port=port)

if __name__ == "__main__":
    main()
