"""
🚀 NIKOH BOT - Railway uchun tayyor
Token: 8219884908:AAHMBf0JP1Cd_w2aGlN_cl_CZmyGoV1gAK4
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# ==================== KONFIGURATSIYA ====================
BOT_TOKEN = "8219884908:AAHMBf0JP1Cd_w2aGlN_cl_CZmyGoV1gAK4"
ADMIN_ID = "5335676431"  # O'zingizning Telegram ID

# ==================== LOGGING ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== BOT ====================
async def main():
    """Asosiy bot funksiyasi"""
    logger.info("=" * 50)
    logger.info("🚀 NIKOH BOT ISHGA TUSHMOQDA...")
    logger.info(f"📱 Token: {BOT_TOKEN[:15]}...")
    logger.info("=" * 50)
    
    # 1. BOT YARATISH
    try:
        bot = Bot(token=BOT_TOKEN)
        # Bot ma'lumotlarini olish
        me = await bot.get_me()
        logger.info(f"✅ Bot yaratildi: @{me.username} ({me.first_name})")
        logger.info(f"🆔 Bot ID: {me.id}")
    except Exception as e:
        logger.error(f"❌ Bot yaratishda xatolik: {e}")
        logger.error("⚠️ Token noto'g'ri yoki internet muammosi")
        return
    
    # 2. DISPATCHER
    dp = Dispatcher(storage=MemoryStorage())
    
    # ==================== KEYBOARDS ====================
    
    def get_main_menu():
        """Asosiy menyu"""
        builder = ReplyKeyboardBuilder()
        builder.row(KeyboardButton(text="👤 Profil"))
        builder.row(KeyboardButton(text="💰 Hisobim"))
        builder.row(KeyboardButton(text="📨 So'rov yuborish"))
        builder.row(KeyboardButton(text="📞 Aloqa"))
        builder.row(KeyboardButton(text="ℹ️ Yordam"))
        return builder.as_markup(resize_keyboard=True)
    
    def get_phone_keyboard():
        """Telefon raqam so'rash"""
        builder = ReplyKeyboardBuilder()
        builder.row(KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True))
        return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    
    # ==================== HANDLERS ====================
    
    @dp.message(CommandStart())
    async def start_command(message: Message, state: FSMContext):
        """/start komandasi"""
        await state.clear()
        
        logger.info(f"📨 /start from {message.from_user.id} (@{message.from_user.username})")
        
        text = """Assalomu alaykum! 👋

Hayrli nikoh botiga xush kelibsiz!

Bu bot orqali:
• Profil to'ldirish
• Anketa joylashtirish
• Boshqa foydalanuvchilar bilan aloqa

Boshlash uchun telefon raqamingizni yuboring:"""
        
        await message.answer(text, reply_markup=get_phone_keyboard())
    
    @dp.message(F.contact)
    async def handle_contact(message: Message, state: FSMContext):
        """Telefon raqam qabul qilish"""
        phone = message.contact.phone_number
        
        logger.info(f"📞 Telefon raqam: {phone} from {message.from_user.id}")
        
        text = f"""✅ Telefon raqamingiz tasdiqlandi!

📱 Raqam: {phone}
👤 Ism: {message.from_user.first_name}

🎉 Tabriklaymiz! Hisobingizga 5 000 so'm bonus qo'shildi!

Endi botning barcha funksiyalaridan foydalanishingiz mumkin."""
        
        await message.answer(text, reply_markup=get_main_menu())
    
    @dp.message(F.text == "👤 Profil")
    async def profile_handler(message: Message):
        """Profil bo'limi"""
        await message.answer("""
📋 **PROFIL TO'LDIRISH**

1. Jinsingizni tanlang:
   - Erkak
   - Ayol

2. Yoshingizni kiriting (18-99)

3. Boshqa ma'lumotlar

Profil to'ldirishni boshlash uchun "Erkak" yoki "Ayol" deb yozing.""")
    
    @dp.message(F.text == "💰 Hisobim")
    async def balance_handler(message: Message):
        """Hisob bo'limi"""
        await message.answer("""
💰 **HISOBINGIZ**

Balans: 5 000 so'm
Bonus: 5 000 so'm
Jami: 10 000 so'm

💳 To'lov usullari:
• Uzcard
• Humo
• USDT (TRC20)
• Visa/Mastercard

To'lov qilish uchun "Hisobni to'ldirish" tugmasini bosing.""")
    
    @dp.message(F.text == "📨 So'rov yuborish")
    async def request_handler(message: Message):
        """So'rov yuborish"""
        await message.answer("""
📨 **SO'ROV YUBORISH**

Anketa raqamini kiriting yoki anketalarni ko'rish uchun "Anketalarni ko'rish" tugmasini bosing.

Anketa raqami @Hayrli_nikoh_kanali kanalidan olinadi.""")
    
    @dp.message(F.text == "📞 Aloqa")
    async def contact_handler(message: Message):
        """Aloqa"""
        await message.answer("""
📞 **ALOQA**

Admin: @Hayrli_nikoh_admin
Kanal: @NIKOH_01
Bot: @Nikoh_uzbot

🕒 Ish vaqti: 24/7
🌐 Platforma: Telegram

Savollar bo'lsa adminga yozing.""")
    
    @dp.message(F.text == "ℹ️ Yordam")
    async def help_handler(message: Message):
        """Yordam"""
        await message.answer("""
ℹ️ **YORDAM**

1. Profil to'ldirish - "👤 Profil"
2. Hisobni to'ldirish - "💰 Hisobim"
3. So'rov yuborish - "📨 So'rov yuborish"
4. Aloqa - "📞 Aloqa"

Qo'shimcha: /start - Botni qayta ishga tushirish
Admin: /admin - Admin paneli (faqat adminlar)""")
    
    @dp.message(Command("admin"))
    async def admin_handler(message: Message):
        """Admin paneli"""
        if str(message.from_user.id) == ADMIN_ID:
            await message.answer("""
🛠 **ADMIN PANELI**

Foydalanuvchilar: /users
Statistika: /stats
Xabar yuborish: /broadcast

Bot holati: ✅ Faol
Foydalanuvchilar: 1
Profil to'ldirganlar: 0""")
        else:
            await message.answer("⚠️ Siz admin emassiz!")
    
    @dp.message()
    async def echo_handler(message: Message):
        """Boshqa barcha xabarlar"""
        if message.text.lower() in ["erkak", "ayol"]:
            await message.answer(f"✅ Jinsingiz: {message.text}. Endi yoshingizni kiriting (18-99):")
        elif message.text.isdigit() and len(message.text) <= 3:
            await message.answer(f"✅ Yosh: {message.text}. Endi bo'yingizni kiriting (sm):")
        else:
            await message.answer(f"📨 Sizning xabaringiz: {message.text}")
    
    # ==================== BOTNI ISHGA TUSHIRISH ====================
    
    logger.info("✅ Barcha handlers yuklandi")
    logger.info("🟢 Bot faol. Xabarlarni kutmoqda...")
    
    try:
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        logger.error(f"❌ Botda xatolik: {e}")
    finally:
        await bot.session.close()
        logger.info("🔴 Bot to'xtatildi")

# ==================== RAILWAY ENTRY POINT ====================
if __name__ == "__main__":
    # Railway uchun
    asyncio.run(main())