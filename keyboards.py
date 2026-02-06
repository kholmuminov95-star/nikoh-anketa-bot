from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, 
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# ==================== REPLY KEYBOARDS ====================

def phone_request_kb():
    """Telefon raqam so'rash tugmasi"""
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(
        text="📱 Telefon raqamni yuborish",
        request_contact=True
    ))
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def main_menu_kb():
    """Asosiy menyu"""
    builder = ReplyKeyboardBuilder()
    
    # Birinchi qator
    builder.row(KeyboardButton(text="💰 Hisobim"))
    builder.row(KeyboardButton(text="👤 Profil"))
    builder.row(KeyboardButton(text="📨 So'rov yuborish"))
    builder.row(KeyboardButton(text="📢 E'lon joylashtirish"))
    builder.row(KeyboardButton(text="🔍 Anketa qidirish"))
    builder.row(KeyboardButton(text="💎 VIP a'zo"))
    builder.row(KeyboardButton(text="🔄 Bosh menyu"))
    
    return builder.as_markup(resize_keyboard=True)

def hisob_menu_kb():
    """Hisob menyusi"""
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="💳 Hisobni to'ldirish"))
    builder.row(KeyboardButton(text="📊 Tranzaksiyalar tarixi"))
    builder.row(KeyboardButton(text="🏠 Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

def gender_kb():
    """Jins tanlash"""
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="👨 Erkak"))
    builder.row(KeyboardButton(text="👩 Ayol"))
    builder.row(KeyboardButton(text="🏠 Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

def yes_no_kb():
    """Ha/Yo'q tugmalari"""
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="✅ Ha"))
    builder.row(KeyboardButton(text="❌ Yo'q"))
    builder.row(KeyboardButton(text="🏠 Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

def nationality_kb():
    """Millat tanlash"""
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="🇺🇿 O'zbek"))
    builder.row(KeyboardButton(text="🇰🇿 Qozoq"))
    builder.row(KeyboardButton(text="🇰🇬 Qirg'iz"))
    builder.row(KeyboardButton(text="🇹🇯 Tojik"))
    builder.row(KeyboardButton(text="🇹🇷 Turk"))
    builder.row(KeyboardButton(text="🇷🇺 Rus"))
    builder.row(KeyboardButton(text="🌍 Boshqa"))
    builder.row(KeyboardButton(text="🏠 Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

def marital_status_male_kb():
    """Erkaklar uchun oilaviy holat"""
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="👤 Bo'ydoq"))
    builder.row(KeyboardButton(text="💔 Ajrashgan"))
    builder.row(KeyboardButton(text="💍 Uylangan"))
    builder.row(KeyboardButton(text="🏠 Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

def marital_status_female_kb():
    """Ayollar uchun oilaviy holat"""
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="👰 Turmush qurmagan"))
    builder.row(KeyboardButton(text="💔 Ajrashgan"))
    builder.row(KeyboardButton(text="⚰️ Beva"))
    builder.row(KeyboardButton(text="🏠 Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

def countries_kb():
    """Mamlakatlar"""
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
    builder.row(KeyboardButton(text="🏠 Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

def regions_kb():
    """Viloyatlar (O'zbekiston uchun)"""
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
    builder.row(KeyboardButton(text="🏠 Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

def second_wife_kb():
    """Ikkinchi xotinlik"""
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="✅ Ha"))
    builder.row(KeyboardButton(text="🤔 O'ylab ko'riladi"))
    builder.row(KeyboardButton(text="❌ Yo'q"))
    builder.row(KeyboardButton(text="🏠 Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

def filled_by_kb():
    """Kim to'ldirdi"""
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="👤 O'zi"))
    builder.row(KeyboardButton(text="👥 Vakili"))
    builder.row(KeyboardButton(text="🏠 Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

def payment_methods_kb():
    """To'lov usullari"""
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="💰 USDT (TRC20)"))
    builder.row(KeyboardButton(text="💳 Visa/Mastercard"))
    builder.row(KeyboardButton(text="💳 Uzcard"))
    builder.row(KeyboardButton(text="💳 Humo"))
    builder.row(KeyboardButton(text="🇷🇺 Rubl"))
    builder.row(KeyboardButton(text="🇹🇷 Turk lirasi"))
    builder.row(KeyboardButton(text="🏠 Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

def ad_types_kb():
    """E'lon turlari"""
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="📋 Oddiy e'lon"))
    builder.row(KeyboardButton(text="⚡ Tezkor e'lon"))
    builder.row(KeyboardButton(text="🏠 Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

# ==================== INLINE KEYBOARDS ====================

def confirm_kb():
    """Tasdiqlash/Rad etish"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="✅ Tasdiqlash", 
        callback_data="confirm"
    ))
    builder.row(InlineKeyboardButton(
        text="❌ Bekor qilish", 
        callback_data="cancel"
    ))
    return builder.as_markup()

def retry_kb():
    """Tasdiqlash/Qayta kiritish"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="✅ Tasdiqlash", 
        callback_data="confirm"
    ))
    builder.row(InlineKeyboardButton(
        text="🔄 Qayta kiritish", 
        callback_data="retry"
    ))
    builder.row(InlineKeyboardButton(
        text="🏠 Bosh menyu", 
        callback_data="main_menu"
    ))
    return builder.as_markup()

def send_request_kb(profile_id):
    """So'rov yuborish"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="📨 So'rov yuborish", 
        callback_data=f"send_request:{profile_id}"
    ))
    return builder.as_markup()