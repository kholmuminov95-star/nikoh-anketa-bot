"""
🚀 NIKOH BOT - To'liq bitta faylda
Telegram: @Nikoh_uzbot
Admin: @Hayrli_nikoh_admin
"""

import os
import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, CallbackQuery, KeyboardButton, 
    ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardRemove
)
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# ==================== KONFIGURATSIYA ====================
BOT_TOKEN = "8219884908:AAHMBf0JP1Cd_w2aGlN_cl_CZmyGoV1gAK4"
ADMIN_ID = 5335676431  # Sizning Telegram ID

# Kurslar va bonuslar
USD_TO_UZS = 12100
BONUS_300K = 0.10  # 10%
BONUS_500K = 0.15  # 15%
BONUS_1M = 0.20    # 20%

# Minimal to'lovlar
MIN_USD = 4
MIN_UZS = 50000

# ==================== LOGGING ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== FSM HOLATLARI ====================
class ProfileStates(StatesGroup):
    # Asosiy ma'lumotlar
    waiting_for_gender = State()
    waiting_for_age = State()
    waiting_for_height = State()
    waiting_for_weight = State()
    waiting_for_nationality = State()
    waiting_for_nationality_custom = State()
    waiting_for_marital_status = State()
    waiting_for_children = State()
    
    # Ayollar uchun qo'shimcha
    waiting_for_hijab = State()
    waiting_for_ready_to_move = State()
    waiting_for_second_wife = State()
    
    # Manzil
    waiting_for_country = State()
    waiting_for_region = State()
    waiting_for_origin_country = State()
    waiting_for_origin_region = State()
    
    # Din va til
    waiting_for_prays = State()
    waiting_for_languages = State()
    
    # Matnli javoblar
    waiting_for_about = State()
    waiting_for_requirements = State()
    waiting_for_filled_by = State()
    
    # Tasdiqlash
    confirming_profile = State()

class PaymentStates(StatesGroup):
    waiting_for_payment_method = State()
    waiting_for_amount_usd = State()
    waiting_for_amount_uzs = State()
    confirming_payment = State()
    waiting_for_receipt = State()

# ==================== KEYBOARD FUNCTIONS ====================
def phone_request_kb():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(
        text="📱 Telefon raqamni yuborish",
        request_contact=True
    ))
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def main_menu_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="💰 Hisobim"))
    builder.row(KeyboardButton(text="👤 Profil"))
    builder.row(KeyboardButton(text="📨 So'rov yuborish"))
    builder.row(KeyboardButton(text="📢 E'lon joylashtirish"))
    builder.row(KeyboardButton(text="💎 VIP a'zo"))
    builder.row(KeyboardButton(text="🔄 Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

def gender_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="👨 Erkak"))
    builder.row(KeyboardButton(text="👩 Ayol"))
    builder.row(KeyboardButton(text="🔄 Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

def yes_no_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="✅ Ha"))
    builder.row(KeyboardButton(text="❌ Yo'q"))
    builder.row(KeyboardButton(text="🔄 Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

def nationality_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="🇺🇿 O'zbek"))
    builder.row(KeyboardButton(text="🇰🇿 Qozoq"))
    builder.row(KeyboardButton(text="🇰🇬 Qirg'iz"))
    builder.row(KeyboardButton(text="🇹🇯 Tojik"))
    builder.row(KeyboardButton(text="🇹🇷 Turk"))
    builder.row(KeyboardButton(text="🇷🇺 Rus"))
    builder.row(KeyboardButton(text="🌍 Boshqa"))
    builder.row(KeyboardButton(text="🔄 Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

def marital_status_male_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="👤 Bo'ydoq"))
    builder.row(KeyboardButton(text="💔 Ajrashgan"))
    builder.row(KeyboardButton(text="💍 Uylangan"))
    builder.row(KeyboardButton(text="🔄 Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

def marital_status_female_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="👰 Turmush qurmagan"))
    builder.row(KeyboardButton(text="💔 Ajrashgan"))
    builder.row(KeyboardButton(text="⚰️ Beva"))
    builder.row(KeyboardButton(text="🔄 Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

def countries_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="🇺🇿 O'zbekiston"))
    builder.row(KeyboardButton(text="🇰🇿 Qozog'iston"))
    builder.row(KeyboardButton(text="🇰🇬 Qirg'iziston"))
    builder.row(KeyboardButton(text="🇹🇯 Tojikiston"))
    builder.row(KeyboardButton(text="🇹🇷 Turkiya"))
    builder.row(KeyboardButton(text="🇺🇿 Qoraqalpog'iston"))
    builder.row(KeyboardButton(text="🇷🇺 Rossiya"))
    builder.row(KeyboardButton(text="🇸🇦 Saudiya"))
    builder.row(KeyboardButton(text="🇪🇬 Misr"))
    builder.row(KeyboardButton(text="🇪🇺 Yevropa"))
    builder.row(KeyboardButton(text="🌍 Boshqa"))
    builder.row(KeyboardButton(text="🔄 Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

def regions_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="🏙️ Toshkent sh."))
    builder.row(KeyboardButton(text="🏙️ Toshkent vil."))
    builder.row(KeyboardButton(text="🏙️ Farg'ona"))
    builder.row(KeyboardButton(text="🏙️ Andijon"))
    builder.row(KeyboardButton(text="🏙️ Namangan"))
    builder.row(KeyboardButton(text="🏙️ Jizzax"))
    builder.row(KeyboardButton(text="🏙️ Sirdaryo"))
    builder.row(KeyboardButton(text="🏙️ Samarqand"))
    builder.row(KeyboardButton(text="🏙️ Qashqadaryo"))
    builder.row(KeyboardButton(text="🏙️ Navoiy"))
    builder.row(KeyboardButton(text="🏙️ Surxondaryo"))
    builder.row(KeyboardButton(text="🏙️ Buxoro"))
    builder.row(KeyboardButton(text="🏙️ Xorazm"))
    builder.row(KeyboardButton(text="🔄 Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

def second_wife_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="✅ Ha"))
    builder.row(KeyboardButton(text="🤔 O'ylab ko'riladi"))
    builder.row(KeyboardButton(text="❌ Yo'q"))
    builder.row(KeyboardButton(text="🔄 Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

def filled_by_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="👤 O'zi"))
    builder.row(KeyboardButton(text="👥 Vakili"))
    builder.row(KeyboardButton(text="🔄 Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

def payment_methods_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="💰 USDT (TRC20)"))
    builder.row(KeyboardButton(text="💳 Visa"))
    builder.row(KeyboardButton(text="💳 Uzcard"))
    builder.row(KeyboardButton(text="💳 Humo"))
    builder.row(KeyboardButton(text="🇷🇺 Rubl"))
    builder.row(KeyboardButton(text="🇹🇷 Turk lirasi"))
    builder.row(KeyboardButton(text="🔄 Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

def confirm_inline_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="confirm"))
    builder.row(InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel"))
    return builder.as_markup()

def retry_inline_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="confirm"))
    builder.row(InlineKeyboardButton(text="🔄 Qayta kiritish", callback_data="retry"))
    builder.row(InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="main_menu"))
    return builder.as_markup()

# ==================== YORDAMCHI FUNKSIYALAR ====================
def calculate_bonus(amount_uzs):
    """Bonusni hisoblash"""
    if amount_uzs >= 1000000:
        return int(amount_uzs * BONUS_1M)
    elif amount_uzs >= 500000:
        return int(amount_uzs * BONUS_500K)
    elif amount_uzs >= 300000:
        return int(amount_uzs * BONUS_300K)
    return 0

def validate_age(text):
    """Yoshni tekshirish"""
    try:
        age = int(text)
        if 18 <= age <= 99:
            return age
        return None
    except:
        return None

def validate_height(text):
    """Bo'yni tekshirish"""
    try:
        height = int(text)
        if 100 <= height <= 250:
            return height
        return None
    except:
        return None

def validate_weight(text):
    """Vaznni tekshirish"""
    try:
        weight = int(text)
        if 30 <= weight <= 200:
            return weight
        return None
    except:
        return None

def validate_languages(text):
    """Tillar sonini tekshirish"""
    try:
        lang = int(text)
        if 1 <= lang <= 10:
            return lang
        return None
    except:
        return None

# ==================== BOT ====================
async def main():
    logger.info("=" * 50)
    logger.info("🚀 NIKOH BOT ISHGA TUSHMOQDA...")
    logger.info(f"📱 Token: {BOT_TOKEN[:15]}...")
    logger.info(f"👑 Admin ID: {ADMIN_ID}")
    logger.info("=" * 50)
    
    # Bot yaratish
    try:
        bot = Bot(token=BOT_TOKEN)
        bot_info = await bot.get_me()
        logger.info(f"✅ Bot yaratildi: @{bot_info.username}")
    except Exception as e:
        logger.error(f"❌ Bot yaratishda xatolik: {e}")
        return
    
    # Dispatcher
    dp = Dispatcher(storage=MemoryStorage())
    
    # Foydalanuvchilar ma'lumotlari (vaqtinchalik)
    users_data = {}
    
    # ==================== HANDLERS ====================
    
    @dp.message(CommandStart())
    async def start_command(message: Message, state: FSMContext):
        """/start komandasi"""
        await state.clear()
        
        logger.info(f"📨 /start from {message.from_user.id}")
        
        text = """Assalomu alaykum! 👋

Hayrli nikoh botiga xush kelibsiz!

📋 **Bot funksiyalari:**
• 👤 Profil to'ldirish
• 💰 Hisobni boshqarish
• 📨 So'rov yuborish
• 📢 E'lon joylashtirish

Boshlash uchun telefon raqamingizni yuboring:"""
        
        await message.answer(text, reply_markup=phone_request_kb())
    
    @dp.message(F.contact)
    async def handle_contact(message: Message, state: FSMContext):
        """Telefon raqam qabul qilish"""
        phone = message.contact.phone_number
        
        logger.info(f"📞 Telefon raqam: {phone}")
        
        # Foydalanuvchi ma'lumotlarini saqlash
        users_data[message.from_user.id] = {
            'phone': phone,
            'first_name': message.from_user.first_name,
            'username': message.from_user.username,
            'balance': 5000,  # Start bonus
            'profile_completed': False
        }
        
        text = f"""✅ **Telefon raqamingiz tasdiqlandi!**

📱 Raqam: {phone}
👤 Ism: {message.from_user.first_name}
🔗 Username: @{message.from_user.username or 'yoq'}

🎉 **Tabriklaymiz!** Hisobingizga 5 000 so'm bonus qo'shildi!

📋 Botning barcha funksiyalaridan to'liq foydalanish uchun iltimos, **Profil** bo'limini to'ldiring.

🔗 **Sizning referal kodingiz:** 
https://t.me/Nikoh_uzbot?start={message.from_user.id}"""
        
        await message.answer(text, reply_markup=main_menu_kb())
    
    @dp.message(F.text == "🔄 Bosh menyu")
    async def main_menu_handler(message: Message, state: FSMContext):
        """Bosh menyuga qaytish"""
        await state.clear()
        await message.answer("🏠 Bosh menyuga qaytdingiz.", reply_markup=main_menu_kb())
    
    @dp.message(F.text == "👤 Profil")
    async def profile_menu(message: Message, state: FSMContext):
        """Profil menyusi"""
        user = users_data.get(message.from_user.id)
        
        if not user or not user.get('profile_completed'):
            text = """ℹ️ **Profil to'ldirish**

Tushunmasangiz videoni ko'rishingiz mumkun:
👉 https://t.me/nikohboti/9

**Jinsingizni tanlang:**"""
            await message.answer(text, reply_markup=gender_kb())
            await state.set_state(ProfileStates.waiting_for_gender)
        else:
            await message.answer("✅ Sizning profilingiz allaqachon to'ldirilgan.", reply_markup=main_menu_kb())
    
    # ==================== PROFIL TO'LDIRISH ====================
    
    @dp.message(ProfileStates.waiting_for_gender, F.text.in_(["👨 Erkak", "👩 Ayol"]))
    async def handle_gender(message: Message, state: FSMContext):
        """Jinsni qabul qilish"""
        gender = "Erkak" if "Erkak" in message.text else "Ayol"
        await state.update_data(gender=gender)
        
        text = """📋 **Profil to'ldirish**

Bu NIKOH platformasi. Anketani faqat valiyingiz (ota-ona, aka-uka) roziligi bilan to'ldiring.

⚠️ Valiysiz e'lon berish dinimizga va odatimizga zid.
🙏 O'zingizga va boshqalarga zulm qilmang.

Profilni to'ldirish orqali siz maxfiy e'lon joylashtirasiz. Raqamingiz va username'ingiz faqat VIP a'zolarga ko'rsatilishi mumkin.

**Yoshingizni kiriting (18-99):**"""
        
        await message.answer(text)
        await state.set_state(ProfileStates.waiting_for_age)
    
    @dp.message(ProfileStates.waiting_for_age)
    async def handle_age(message: Message, state: FSMContext):
        """Yoshni qabul qilish"""
        if message.text == "🔄 Bosh menyu":
            await main_menu_handler(message, state)
            return
        
        age = validate_age(message.text)
        if not age:
            await message.answer("⚠️ Iltimos, 18-99 oralig'ida bo'lgan yoshingizni kiriting:")
            return
        
        await state.update_data(age=age)
        await message.answer("**Bo'yingizni kiriting (100-250 sm):**")
        await state.set_state(ProfileStates.waiting_for_height)
    
    @dp.message(ProfileStates.waiting_for_height)
    async def handle_height(message: Message, state: FSMContext):
        """Bo'yni qabul qilish"""
        if message.text == "🔄 Bosh menyu":
            await main_menu_handler(message, state)
            return
        
        height = validate_height(message.text)
        if not height:
            await message.answer("⚠️ Bo'y 100-250 sm oralig'ida bo'lishi kerak:")
            return
        
        await state.update_data(height=height)
        await message.answer("**Vazningizni kiriting (30-200 kg):**")
        await state.set_state(ProfileStates.waiting_for_weight)
    
    @dp.message(ProfileStates.waiting_for_weight)
    async def handle_weight(message: Message, state: FSMContext):
        """Vaznni qabul qilish"""
        if message.text == "🔄 Bosh menyu":
            await main_menu_handler(message, state)
            return
        
        weight = validate_weight(message.text)
        if not weight:
            await message.answer("⚠️ Vazn 30-200 kg oralig'ida bo'lishi kerak:")
            return
        
        await state.update_data(weight=weight)
        await message.answer("**Millatingizni tanlang:**", reply_markup=nationality_kb())
        await state.set_state(ProfileStates.waiting_for_nationality)
    
    @dp.message(ProfileStates.waiting_for_nationality)
    async def handle_nationality(message: Message, state: FSMContext):
        """Millatni qabul qilish"""
        if message.text == "🔄 Bosh menyu":
            await main_menu_handler(message, state)
            return
        
        if message.text == "🌍 Boshqa":
            await message.answer("**Millatingizni kiriting:**")
            await state.set_state(ProfileStates.waiting_for_nationality_custom)
            return
        
        await state.update_data(nationality=message.text)
        data = await state.get_data()
        
        if data['gender'] == "Erkak":
            await message.answer("**Oilaviy holatingizni tanlang:**", reply_markup=marital_status_male_kb())
        else:
            await message.answer("**Oilaviy holatingizni tanlang:**", reply_markup=marital_status_female_kb())
        
        await state.set_state(ProfileStates.waiting_for_marital_status)
    
    @dp.message(ProfileStates.waiting_for_nationality_custom)
    async def handle_nationality_custom(message: Message, state: FSMContext):
        """Maxsus millatni qabul qilish"""
        if message.text == "🔄 Bosh menyu":
            await main_menu_handler(message, state)
            return
        
        await state.update_data(nationality=message.text)
        data = await state.get_data()
        
        if data['gender'] == "Erkak":
            await message.answer("**Oilaviy holatingizni tanlang:**", reply_markup=marital_status_male_kb())
        else:
            await message.answer("**Oilaviy holatingizni tanlang:**", reply_markup=marital_status_female_kb())
        
        await state.set_state(ProfileStates.waiting_for_marital_status)
    
    @dp.message(ProfileStates.waiting_for_marital_status)
    async def handle_marital_status(message: Message, state: FSMContext):
        """Oilaviy holatni qabul qilish"""
        if message.text == "🔄 Bosh menyu":
            await main_menu_handler(message, state)
            return
        
        status_map = {
            "👤 Bo'ydoq": "Bo'ydoq",
            "💔 Ajrashgan": "Ajrashgan", 
            "💍 Uylangan": "Uylangan",
            "👰 Turmush qurmagan": "Turmush qurmagan",
            "⚰️ Beva": "Beva"
        }
        
        marital_status = status_map.get(message.text, message.text)
        await state.update_data(marital_status=marital_status)
        
        # Agar ajrashgan yoki beva bo'lsa, farzandlar sonini so'rash
        if marital_status in ["Ajrashgan", "Beva"]:
            await message.answer("**Farzandlaringiz sonini kiriting (0-10, yo'q bo'lsa 0):**")
            await state.set_state(ProfileStates.waiting_for_children)
        else:
            await state.update_data(children=0)
            await handle_children_next(message, state)
    
    async def handle_children_next(message: Message, state: FSMContext):
        """Farzandlar keyingi bosqich"""
        data = await state.get_data()
        
        if data['gender'] == "Ayol":
            await message.answer("**Ro'mol o'raysizmi?**", reply_markup=yes_no_kb())
            await state.set_state(ProfileStates.waiting_for_hijab)
        else:
            await message.answer("**Manzilingizni tanlang:**", reply_markup=countries_kb())
            await state.set_state(ProfileStates.waiting_for_country)
    
    @dp.message(ProfileStates.waiting_for_children)
    async def handle_children(message: Message, state: FSMContext):
        """Farzandlar sonini qabul qilish"""
        if message.text == "🔄 Bosh menyu":
            await main_menu_handler(message, state)
            return
        
        try:
            children = int(message.text)
            if 0 <= children <= 10:
                await state.update_data(children=children)
                await handle_children_next(message, state)
            else:
                await message.answer("⚠️ Farzandlar soni 0-10 oralig'ida bo'lishi kerak:")
        except:
            await message.answer("⚠️ Iltimos, raqam kiriting (0-10):")
    
    # Ayollar uchun qo'shimcha savollar
    @dp.message(ProfileStates.waiting_for_hijab)
    async def handle_hijab(message: Message, state: FSMContext):
        """Ro'mol haqida"""
        if message.text == "🔄 Bosh menyu":
            await main_menu_handler(message, state)
            return
        
        hijab = message.text == "✅ Ha"
        await state.update_data(hijab=hijab)
        await message.answer("**Ko'chib o'tishga tayyormisiz?**", reply_markup=yes_no_kb())
        await state.set_st