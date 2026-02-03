import logging
import random
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

# ================= CONFIG =================
BOT_TOKEN = "8219884908:AAHMBf0JP1Cd_w2aGlN_cl_CZmyGoV1gAK4"
ADMIN_ID = 123456789  # <-- sening admin user ID raqam ko‘rinishda
START_BALANCE = 5000  # boshlang'ich bonus

# ================= LOGGING =================
logging.basicConfig(level=logging.INFO)

# ================= BOT & STORAGE =================
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ================= DATA =================
users = {}  # {user_id: {phone, balance, referal_code, profile, anketa_stage}}
transactions = []  # {user_id, type, amount, timestamp}
anketas = {}  # {user_id: profile_data}

# ================= STATES =================
class ProfileStates(StatesGroup):
    gender = State()
    age = State()
    height = State()
    weight = State()
    nationality = State()
    custom_nationality = State()
    marital = State()
    children = State()
    location_country = State()
    location_region = State()
    pray = State()
    languages = State()
    about = State()
    partner_requirements = State()
    filled_by = State()
    confirm = State()

# ================= KEYBOARDS =================
def start_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("/tel", request_contact=True))
    return kb

def main_menu_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("/hisobim", "/profil")
    kb.add("/vip_azo", "/pul_topish")
    kb.add("/adminga_xabar", "/bosh_menyu")
    return kb

def gender_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("/erkak", "/ayol", "/bosh_menyu")
    return kb

def marital_keyboard(is_female=False):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    if is_female:
        kb.add("Turmush qurmagan", "Ajrashgan", "Beva", "/bosh_menyu")
    else:
        kb.add("Bo'ydoq", "Ajrashgan", "Uylangan", "/bosh_menyu")
    return kb

def yes_no_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("Ha", "Yo'q", "/bosh_menyu")
    return kb

def confirm_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Tasdiqlash", callback_data="confirm"))
    kb.add(InlineKeyboardButton("Qayta kiritish", callback_data="retry"))
    kb.add(InlineKeyboardButton("Bosh menyu", callback_data="main_menu"))
    return kb

# ================= HANDLERS =================
@dp.message(commands=["start"])
async def cmd_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id not in users:
        referal_code = f"{random.randint(10000,99999)}"
        users[user_id] = {
            "phone": None,
            "balance": START_BALANCE,
            "referal_code": referal_code,
            "profile": {},
            "anketa_stage": None
        }
    await message.answer(
        "Botdan foydalanish uchun telefon raqamingizni yuboring:",
        reply_markup=start_keyboard()
    )

@dp.message(Text(equals="/tel"))
async def request_contact(message: types.Message):
    await message.answer("Telefon raqamingizni yuboring:")

@dp.message(content_types=types.ContentType.CONTACT)
async def contact_handler(message: types.Message):
    user_id = message.from_user.id
    phone = message.contact.phone_number
    users[user_id]["phone"] = phone
    await message.answer(
        f"📱 Telefon raqamingiz tasdiqlandi!\n"
        f"@NIKOH_01 kanalining rasmiy botiga xush kelibsiz.\n\n"
        f"🎉 Tabriklaymiz! Hisobingizga {START_BALANCE} so‘m bonus qo‘shildi!\n\n"
        f"Sizning referal kodingiz: https://t.me/Nikoh_uzbot?start={users[user_id]['referal_code']}",
        reply_markup=main_menu_keyboard()
    )

# ================= PROFIL ANKETA =================
@dp.message(commands=["profil"])
async def start_profile(message: types.Message, state: FSMContext):
    await message.answer("Jinsingizni tanlang:", reply_markup=gender_keyboard())
    await state.set_state(ProfileStates.gender)

@dp.message(ProfileStates.gender)
async def gender_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    gender = message.text.lower()
    if gender not in ["erkak","ayol"]:
        await message.answer("Faqat /erkak yoki /ayol ni tanlang!")
        return
    users[user_id]["profile"]["gender"] = gender
    await message.answer("Yoshingizni kiriting (18-99):")
    await state.set_state(ProfileStates.age)

@dp.message(ProfileStates.age)
async def age_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not message.text.isdigit():
        await message.answer("Faqat raqam kiriting!")
        return
    age = int(message.text)
    if not 18 <= age <= 99:
        await message.answer("Yosh 18-99 oralig‘ida bo‘lishi kerak!")
        return
    users[user_id]["profile"]["age"] = age
    await message.answer("Bo‘yingizni kiriting (100-250 sm):")
    await state.set_state(ProfileStates.height)

@dp.message(ProfileStates.height)
async def height_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not message.text.isdigit():
        await message.answer("Faqat raqam kiriting!")
        return
    height = int(message.text)
    if not 100 <= height <= 250:
        await message.answer("Bo‘y 100-250 sm oralig‘ida bo‘lishi kerak!")
        return
    users[user_id]["profile"]["height"] = height
    await message.answer("Vazningizni kiriting (30-200 kg):")
    await state.set_state(ProfileStates.weight)

@dp.message(ProfileStates.weight)
async def weight_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not message.text.isdigit():
        await message.answer("Faqat raqam kiriting!")
        return
    weight = int(message.text)
    if not 30 <= weight <= 200:
        await message.answer("Vazn 30-200 kg oralig‘ida bo‘lishi kerak!")
        return
    users[user_id]["profile"]["weight"] = weight
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("O'zbek","Qozoq","Qirg'iz","Tojik","Turk","Rus","Boshqa","/bosh_menyu")
    await message.answer("Millatingizni tanlang:", reply_markup=kb)
    await state.set_state(ProfileStates.nationality)

# ================= RUN =================
if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
