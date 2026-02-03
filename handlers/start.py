from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from database import Database
from keyboards import phone_request_kb, main_menu_kb
from config import ADMIN_ID

router = Router()
db = Database()

@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await state.clear()
    
    # Agar telefon raqam bo'lsa
    user = await db.get_user(message.from_user.id)
    if user and user.get('phone'):
        text = "Assalomu alaykum! Hayrli nikoh botiga xush kelibsiz."
        await message.answer(text, reply_markup=main_menu_kb())
    else:
        text = "Botdan foydalanish uchun telefon raqamingizni kontakt sifatida yuboring:"
        await message.answer(text, reply_markup=phone_request_kb())

@router.message(F.contact)
async def handle_contact(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    
    # Foydalanuvchini qo'shish
    await db.add_user(
        user_id=message.from_user.id,
        phone=phone,
        first_name=message.from_user.first_name,
        username=message.from_user.username
    )
    
    # Bonus berish (faqat birinchi marta)
    user = await db.get_user(message.from_user.id)
    if not user.get('bonus_received'):
        await db.update_balance(
            user_id=message.from_user.id,
            amount=5000,
            transaction_type="bonus",
            description="Start bonus"
        )
        bonus_text = "\n?? Tabriklaymiz! Hisobingizga 5 000 so'm bonus qo'shildi!"
    else:
        bonus_text = ""
    
    text = f"""? Telefon raqamingiz tasdiqlandi! @NIKOH_01 kanalining rasmiy botiga xush kelibsiz.{bonus_text}

?? Botning barcha funksiyalaridan to'liq foydalanish uchun iltimos, ?? Profil bo'limini to'ldiring.

Sizning referal kodingiz: https://t.me/Nikoh_uzbot?start={message.from_user.id}"""
    
    await message.answer(text, reply_markup=main_menu_kb())

@router.message(F.text == "Bosh menyu")
async def main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Bosh menyuga qaytdingiz.", reply_markup=main_menu_kb())

@router.message(F.text == "Hisobim")
async def my_balance(message: Message):
    balance = await db.get_user_balance(message.from_user.id)
    usd = balance / 12100
    
    text = f"""Hisobingiz:
Balans: {balance:,} so'm (${usd:.2f})
1$ = 12,100 so'm

?? Hisobdagi mablag' kartaga qaytarilmaydi, boshqa foydalanuvchiga o'tkazilmaydi. Faqat ichki xizmatlarga (so'rov yuborish, e'lon berish, VIP olish, lichka ochish va h.k.) ishlatiladi."""
    
    from keyboards import ReplyKeyboardBuilder, KeyboardButton
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Hisobni to'ldirish"))
    builder.row(KeyboardButton(text="Tranzaksiyalar tarixi"))
    builder.row(KeyboardButton(text="Bosh menyu"))
    
    await message.answer(text, reply_markup=builder.as_markup(resize_keyboard=True))

@router.message(F.text == "Profil")
async def profile_menu(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    
    if not user.get('profile_completed'):
        text = """Tushunmasangiz videoni ko'rishingiz mumkun --> https://t.me/nikohboti/9
Jinsingizni tanlang:"""
        from keyboards import gender_kb
        await message.answer(text, reply_markup=gender_kb())
    else:
        # Profilni ko'rsatish
        text = "Profil ma'lumotlaringiz:\n\n"
        # Profil ma'lumotlarini formatlash
        await message.answer(text, reply_markup=main_menu_kb())
