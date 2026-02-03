from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# Asosiy menyu
def main_menu_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Hisobim"))
    builder.row(KeyboardButton(text="Profil"))
    builder.row(KeyboardButton(text="So'rov yuborish"))
    builder.row(KeyboardButton(text="E'lon joylashtirish"))
    builder.row(KeyboardButton(text="Yashirin anketalar"))
    builder.row(KeyboardButton(text="Anketa qidirish"))
    builder.row(KeyboardButton(text="Chatlarim"))
    builder.row(KeyboardButton(text="Yangi so'rovlar"))
    builder.row(KeyboardButton(text="Vip a'zo"))
    builder.row(KeyboardButton(text="Pul topish"))
    builder.row(KeyboardButton(text="Adminga xabar"))
    builder.row(KeyboardButton(text="Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

# Telefon raqam so'rash
def phone_request_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Telefon raqamni yuborish", request_contact=True))
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

# Jins tanlash
def gender_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Erkak"))
    builder.row(KeyboardButton(text="Ayol"))
    builder.row(KeyboardButton(text="Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

# Ha/Yo'q
def yes_no_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Ha"))
    builder.row(KeyboardButton(text="Yo'q"))
    builder.row(KeyboardButton(text="Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

# Millatlar
def nationality_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="O'zbek"))
    builder.row(KeyboardButton(text="Qozoq"))
    builder.row(KeyboardButton(text="Qirg'iz"))
    builder.row(KeyboardButton(text="Tojik"))
    builder.row(KeyboardButton(text="Turk"))
    builder.row(KeyboardButton(text="Rus"))
    builder.row(KeyboardButton(text="Boshqa"))
    builder.row(KeyboardButton(text="Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

# Erkaklar uchun oilaviy holat
def marital_status_male_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Bo'ydoq"))
    builder.row(KeyboardButton(text="Ajrashgan"))
    builder.row(KeyboardButton(text="Uylangan"))
    builder.row(KeyboardButton(text="Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

# Ayollar uchun oilaviy holat
def marital_status_female_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Turmush qurmagan"))
    builder.row(KeyboardButton(text="Ajrashgan"))
    builder.row(KeyboardButton(text="Beva"))
    builder.row(KeyboardButton(text="Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

# Mamlakatlar
def countries_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="O'zbekiston"))
    builder.row(KeyboardButton(text="Qozog'iston"))
    builder.row(KeyboardButton(text="Qirg'iziston"))
    builder.row(KeyboardButton(text="Tojikiston"))
    builder.row(KeyboardButton(text="Turkiya"))
    builder.row(KeyboardButton(text="Qoraqalpog'iston"))
    builder.row(KeyboardButton(text="Rossiya"))
    builder.row(KeyboardButton(text="Saudiya"))
    builder.row(KeyboardButton(text="Misr"))
    builder.row(KeyboardButton(text="Yevropa"))
    builder.row(KeyboardButton(text="Boshqa"))
    builder.row(KeyboardButton(text="Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

# Viloyatlar
def regions_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Toshkent sh."))
    builder.row(KeyboardButton(text="Toshkent vil."))
    builder.row(KeyboardButton(text="Farg'ona"))
    builder.row(KeyboardButton(text="Andijon"))
    builder.row(KeyboardButton(text="Namangan"))
    builder.row(KeyboardButton(text="Jizzax"))
    builder.row(KeyboardButton(text="Sirdaryo"))
    builder.row(KeyboardButton(text="Samarqand"))
    builder.row(KeyboardButton(text="Qashqadaryo"))
    builder.row(KeyboardButton(text="Navoiy"))
    builder.row(KeyboardButton(text="Surxondaryo"))
    builder.row(KeyboardButton(text="Buxoro"))
    builder.row(KeyboardButton(text="Xorazm"))
    builder.row(KeyboardButton(text="Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

# To'lov usullari
def payment_methods_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="USDT (TRC20)"))
    builder.row(KeyboardButton(text="Rubl"))
    builder.row(KeyboardButton(text="Visa"))
    builder.row(KeyboardButton(text="Uzcard"))
    builder.row(KeyboardButton(text="Humo"))
    builder.row(KeyboardButton(text="Turk lira"))
    builder.row(KeyboardButton(text="Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

# E'lon turlari
def ad_types_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Oddiy e'lon joylashtirish"))
    builder.row(KeyboardButton(text="Tezkor e'lon joylashtirish"))
    builder.row(KeyboardButton(text="Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

# Ikkinchi xotinlik
def second_wife_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Ha"))
    builder.row(KeyboardButton(text="O'ylab ko'riladi"))
    builder.row(KeyboardButton(text="Yo'q"))
    builder.row(KeyboardButton(text="Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

# Kim to'ldirdi
def filled_by_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="O'zi"))
    builder.row(KeyboardButton(text="Vakili"))
    builder.row(KeyboardButton(text="Bosh menyu"))
    return builder.as_markup(resize_keyboard=True)

# Inline tugmalar
def confirm_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="confirm"))
    builder.row(InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel"))
    return builder.as_markup()

def retry_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="confirm"))
    builder.row(InlineKeyboardButton(text="🔄 Qayta kiritish", callback_data="retry"))
    builder.row(InlineKeyboardButton(text="🏠 Bosh menyu", callback_data="main_menu"))
    return builder.as_markup()

def send_request_kb(profile_id):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="📨 So'rov yuborish", callback_data=f"send_request:{profile_id}"))
    return builder.as_markup()
