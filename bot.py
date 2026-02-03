import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

TOKEN = "8219884908:AAHMBf0JP1Cd_w2aGlN_cl_CZmyGoV1gAK4"
ADMIN = "@Hayrli_nikoh_admin"

# Storage va dispatcher
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=storage)

# Statelar (FSM)
class Form(StatesGroup):
    purpose = State()
    candidate = State()
    phone = State()

# Start komandasi
@dp.message(Command("start"))
async def start(message: types.Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Lotin")]], resize_keyboard=True
    )
    await message.answer("Assalomu alaykum! Anketani to'ldirishni boshlash uchun 'Lotin' tugmasini bosing.", reply_markup=kb)

# Lotin tugmasi bosilganda
@dp.message(lambda msg: msg.text == "Lotin")
async def lotin_start(message: types.Message, state: FSMContext):
    await message.answer("Anketa to‘ldirishdan maqsadingiz nima?")
    await state.set_state(Form.purpose)

# Maqsad javobi
@dp.message(Form.purpose)
async def process_purpose(message: types.Message, state: FSMContext):
    await state.update_data(purpose=message.text)
    await message.answer("Sizning nomzodingiz kim?")
    await state.set_state(Form.candidate)

# Nomzod javobi
@dp.message(Form.candidate)
async def process_candidate(message: types.Message, state: FSMContext):
    await state.update_data(candidate=message.text)
    await message.answer("Telefon raqamingizni kiriting:")
    await state.set_state(Form.phone)

# Telefon javobi va adminga yuborish
@dp.message(Form.phone)
async def process_phone(message: types.Message, state: FSMContext):
    data = await state.get_data()
    purpose = data.get("purpose")
    candidate = data.get("candidate")
    phone = message.text
    
    text = f"Yangi anketa:\nMaqsad: {purpose}\nNomzod: {candidate}\nTelefon: {phone}"
    
    # Adminga yuborish
    await bot.send_message(chat_id=ADMIN, text=text)
    
    await message.answer("Anketangiz qabul qilindi! Rahmat.")
    await state.clear()

# Botni ishga tushurish
async def main():
    print("Bot ishlayapti...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
