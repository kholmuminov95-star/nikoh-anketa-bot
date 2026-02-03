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
    """Start komandasi"""
    await state.clear()
    
    logger = logging.getLogger(__name__)
    logger.info(f"Start komandasi: {message.from_user.id}")
    
    # Foydalanuvchini tekshirish
    user = await db.get_user(message.from_user.id)
    
    if user and user.get('phone'):
        text = "Assalomu alaykum! Hayrli nikoh botiga xush kelibsiz."
        await message.answer(text, reply_markup=main_menu_kb())
    else:
        text = "Botdan foydalanish uchun telefon raqamingizni kontakt sifatida yuboring:"
        await message.answer(text, reply_markup=phone_request_kb())

@router.message(F.contact)
async def handle_contact(message: Message, state: FSMContext):
    """Telefon raqam qabul qilish"""
    phone = message.contact.phone_number
    
    await db.add_user(
        user_id=message.from_user.id,
        phone=phone,
        first_name=message.from_user.first_name,
        username=message.from_user.username
    )
    
    # Bonus berish
    user = await db.get_user(message.from_user.id)
    if user and not user.get('bonus_received'):
        await db.update_balance(
            user_id=message.from_user.id,
            amount=5000,
            transaction_type="bonus",
            description="Start bonus"
        )
        bonus_text = "\n🎉 Tabriklaymiz! Hisobingizga 5 000 so'm bonus qo'shildi!"
    else:
        bonus_text = ""
    
    text = f"""✅ Telefon raqamingiz tasdiqlandi! @NIKOH_01 kanalining rasmiy botiga xush kelibsiz.{bonus_text}

📋 Botning barcha funksiyalaridan to'liq foydalanish uchun iltimos, Profil bo'limini to'ldiring.

🔗 Sizning referal kodingiz: https://t.me/Nikoh_uzbot?start={message.from_user.id}"""
    
    await message.answer(text, reply_markup=main_menu_kb())

@router.message(F.text == "Bosh menyu")
async def main_menu_handler(message: Message, state: FSMContext):
    """Bosh menyuga qaytish"""
    await state.clear()
    await message.answer("🏠 Bosh menyuga qaytdingiz.", reply_markup=main_menu_kb())
