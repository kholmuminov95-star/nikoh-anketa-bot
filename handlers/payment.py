from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, PhotoSize
from aiogram.fsm.context import FSMContext

from database import Database
from states import PaymentStates
from keyboards import *
from utils import calculate_bonus
from config import *

router = Router()
db = Database()

async def main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🏠 Bosh menyuga qaytdingiz.", reply_markup=main_menu_kb())

@router.message(F.text == "Hisobni to'ldirish")
async def payment_start(message: Message, state: FSMContext):
    text = """💳 **Hisobni to'ldirish**

Quyidagi to'lov usullaridan birini tanlang. Har bir usul uchun minimal summa va bonuslar haqida ma'lumot tanlaganingizdan so'ng ko'rsatiladi.

🎁 **Bonuslar:**
• 300,000 so'mdan yuqori: 10% bonus
• 500,000 so'mdan yuqori: 15% bonus
• 1,000,000 so'mdan yuqori: 20% bonus

⚠️ **Eslatma:** To'lov qilinganidan so'ng mablag' kartaga qaytarilmaydi, boshqa foydalanuvchilarga o'tkazilmaydi. Faqat ichki xizmatlarga (so'rov yuborish, e'lon berish, VIP olish, lichka ochish va h.k.) ishlatiladi."""
    
    await message.answer(text, reply_markup=payment_methods_kb())
    await state.set_state(PaymentStates.waiting_for_payment_method)

# USDT to'lovi
@router.message(PaymentStates.waiting_for_payment_method, F.text == "USDT (TRC20)")
async def payment_usdt(message: Message, state: FSMContext):
    await state.update_data(payment_method="USDT", currency="USD", min_amount=MIN_USD)
    
    text = """💳 **To'lov usuli: USDT (TRC20)**
💰 Valyuta: USD
📊 Minimal summa: 4 USD

🎁 **Bonuslar haqida:**
• 300,000 so'm (24.79 USD) dan yuqori: 10% bonus
• 500,000 so'm (41.32 USD) dan yuqori: 15% bonus
• 1,000,000 so'm (82.64 USD) dan yuqori: 20% bonus

📝 **Misollar:**
• 24.79 USD to'lov: 10% bonus (+2.48 USD), jami 27.27 USD
• 41.32 USD to'lov: 15% bonus (+6.20 USD), jami 47.52 USD
• 82.64 USD to'lov: 20% bonus (+16.53 USD), jami 99.17 USD

💵 **Qancha to'lov qilmoqchisiz? (USDda, eng kam 4 USD):**"""
    
    await message.answer(text)
    await state.set_state(PaymentStates.waiting_for_amount_usd)

@router.message(PaymentStates.waiting_for_amount_usd, F.text)
async def handle_amount_usd(message: Message, state: FSMContext):
    if message.text == "Bosh menyu":
        await main_menu(message, state)
        return
    
    try:
        amount = float(message.text.replace(',', '.'))
        if amount < MIN_USD:
            await message.answer(f"⚠️ Minimal summa {MIN_USD} USD. Iltimos, qaytadan kiriting:")
            return
        
        amount_uzs = int(amount * USD_TO_UZS)
        bonus = calculate_bonus(amount_uzs)
        total_uzs = amount_uzs + bonus
        total_usd = total_uzs / USD_TO_UZS
        
        bonus_percent = int((bonus / amount_uzs * 100)) if amount_uzs > 0 else 0
        
        await state.update_data(
            amount=amount,
            amount_uzs=amount_uzs,
            bonus=bonus,
            total_uzs=total_uzs,
            total_usd=total_usd
        )
        
        text = f"""📋 **To'lov ma'lumotlari:**

💵 To'lov summasi: {amount:.2f} USD
🎁 Bonus: {bonus_percent}% ({bonus:,} so'm)
💰 Hisobingizga tushadi: {total_uzs:,} so'm (${total_usd:.2f})

✅ Tasdiqlaysizmi?"""
        
        await message.answer(text, reply_markup=confirm_kb())
        await state.set_state(PaymentStates.confirming_payment)
        
    except ValueError:
        await message.answer("⚠️ Iltimos, raqam kiriting (masalan: 4, 10, 24.79):")

# So'm to'lovlari (Uzcard, Humo, Rubl)
@router.message(PaymentStates.waiting_for_payment_method, F.text.in_(["Uzcard", "Humo", "Rubl"]))
async def payment_uzs(message: Message, state: FSMContext):
    payment_method = message.text
    await state.update_data(payment_method=payment_method, currency="UZS", min_amount=MIN_UZS)
    
    if payment_method == "Rubl":
        currency_text = "so'm (Rubl bo'yicha)"
        min_text = "50,000 so'm"
    else:
        currency_text = "so'm"
        min_text = "50,000 so'm"
    
    text = f"""💳 **To'lov usuli: {payment_method}**
💰 Valyuta: {currency_text}
📊 Minimal summa: {min_text}

🎁 **Bonuslar haqida:**
• 300,000 so'm (24.79 USD) dan yuqori: 10% bonus
• 500,000 so'm (41.32 USD) dan yuqori: 15% bonus
• 1,000,000 so'm (82.64 USD) dan yuqori: 20% bonus

📝 **Misollar:**
• 300,000 so'm to'lov: 10% bonus (+30,000 so'm), jami 330,000 so'm
• 500,000 so'm to'lov: 15% bonus (+75,000 so'm), jami 575,000 so'm
• 1,000,000 so'm to'lov: 20% bonus (+200,000 so'm), jami 1,200,000 so'm

💵 **Qancha to'lov qilmoqchisiz? (so'mda, eng kam 50,000 so'm):**"""
    
    await message.answer(text)
    await state.set_state(PaymentStates.waiting_for_amount_uzs)

@router.message(PaymentStates.waiting_for_amount_uzs, F.text)
async def handle_amount_uzs(message: Message, state: FSMContext):
    if message.text == "Bosh menyu":
        await main_menu(message, state)
        return
    
    try:
        amount = int(message.text.replace(',', '').replace(' ', ''))
        if amount < MIN_UZS:
            await message.answer(f"⚠️ Minimal summa {MIN_UZS:,} so'm. Iltimos, qaytadan kiriting:")
            return
        
        bonus = calculate_bonus(amount)
        total = amount + bonus
        
        bonus_percent = int((bonus / amount * 100)) if amount > 0 else 0
        
        await state.update_data(
            amount=amount,
            amount_uzs=amount,
            bonus=bonus,
            total_uzs=total
        )
        
        text = f"""📋 **To'lov ma'lumotlari:**

💵 To'lov summasi: {amount:,} so'm
🎁 Bonus: {bonus_percent}% ({bonus:,} so'm)
💰 Hisobingizga tushadi: {total:,} so'm

✅ Tasdiqlaysizmi?"""
        
        await message.answer(text, reply_markup=confirm_kb())
        await state.set_state(PaymentStates.confirming_payment)
        
    except ValueError:
        await message.answer("⚠️ Iltimos, raqam kiriting (masalan: 50000, 300000, 1000000):")

# Visa to'lovi
@router.message(PaymentStates.waiting_for_payment_method, F.text == "Visa")
async def payment_visa(message: Message, state: FSMContext):
    await state.update_data(payment_method="Visa", currency="USD", min_amount=MIN_USD)
    
    text = """💳 **To'lov usuli: Visa**
💰 Valyuta: USD
📊 Minimal summa: 4 USD

🎁 **Bonuslar haqida:**
• 300,000 so'm (24.79 USD) dan yuqori: 10% bonus
• 500,000 so'm (41.32 USD) dan yuqori: 15% bonus
• 1,000,000 so'm (82.64 USD) dan yuqori: 20% bonus

📝 **Misollar:**
• 24.79 USD to'lov: 10% bonus (+2.48 USD), jami 27.27 USD
• 41.32 USD to'lov: 15% bonus (+6.20 USD), jami 47.52 USD
• 82.64 USD to'lov: 20% bonus (+16.53 USD), jami 99.17 USD

💵 **Qancha to'lov qilmoqchisiz? (USDda, eng kam 4 USD):**"""
    
    await message.answer(text)
    await state.set_state(PaymentStates.waiting_for_amount_usd)

# Turk lirasi
@router.message(PaymentStates.waiting_for_payment_method, F.text == "Turk lira")
async def payment_try(message: Message, state: FSMContext):
    await state.update_data(payment_method="Turk lira", currency="TRY", min_amount=MIN_TRY)
    
    text = """💳 **To'lov usuli: Turk lira**
💰 Valyuta: so'm (Turk lira bo'yicha)
📊 Minimal summa: 50,000 so'm (500 Turk lira)

🎁 **Bonuslar haqida:**
• 300,000 so'm (24.79 USD) dan yuqori: 10% bonus
• 500,000 so'm (41.32 USD) dan yuqori: 15% bonus
• 1,000,000 so'm (82.64 USD) dan yuqori: 20% bonus

📝 **Misollar:**
• 300,000 so'm to'lov: 10% bonus (+30,000 so'm), jami 330,000 so'm
• 500,000 so'm to'lov: 15% bonus (+75,000 so'm), jami 575,000 so'm
• 1,000,000 so'm to'lov: 20% bonus (+200,000 so'm), jami 1,200,000 so'm

💵 **Qancha to'lov qilmoqchisiz? (so'mda, eng kam 50,000 so'm):**"""
    
    await message.answer(text)
    await state.set_state(PaymentStates.waiting_for_amount_uzs)

# Tasdiqlash
@router.callback_query(PaymentStates.confirming_payment, F.data == "confirm")
async def confirm_payment(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    
    payment_details = {
        "USDT": "USDT (TRC20) to'lovi uchun rekvizitlar",
        "Visa": "Visa/Mastercard to'lovi uchun rekvizitlar",
        "Uzcard": "Uzcard to'lovi uchun rekvizitlar",
        "Humo": "Humo to'lovi uchun rekvizitlar",
        "Rubl": "Rubl to'lovi uchun rekvizitlar",
        "Turk lira": "Turk lira to'lovi uchun rekvizitlar"
    }
    
    details = payment_details.get(data['payment_method'], "Admin bilan bog'laning")
    
    text = f"""💳 **To'lov uchun rekvizitlar:**

📋 To'lov usuli: {data['payment_method']}
📝 Rekvizitlar: {details}
👤 Ism Familiya/teg: . . 
💵 Summa: {data['amount']} {data['currency']}

⚠️ Iltimos, to'lovni amalga oshirib, chekni rasm ko'rinishida yuboring."""
    
    await callback.message.answer(text)
    await callback.message.answer("📸 Chekni yuboring yoki bosh menyuga qayting:", reply_markup=main_menu_kb())
    await state.set_state(PaymentStates.waiting_for_receipt)

@router.callback_query(PaymentStates.confirming_payment, F.data == "cancel")
async def cancel_payment(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("❌ To'lov bekor qilindi.")
    await callback.message.answer("🏠 Bosh menyuga qaytdingiz.", reply_markup=main_menu_kb())
    await state.clear()

# Chek qabul qilish
@router.message(PaymentStates.waiting_for_receipt, F.photo)
async def handle_receipt(message: Message, state: FSMContext):
    data = await state.get_data()
    photo_id = message.photo[-1].file_id
    
    # Ma'lumotlarni saqlash
    await db.update_balance(
        user_id=message.from_user.id,
        amount=0,  # Hozircha 0, admin tasdiqlagach qo'shiladi
        transaction_type="payment_pending",
        description=f"To'lov kutilmoqda: {data['payment_method']}, {data['amount']} {data['currency']}"
    )
    
    await message.answer("✅ Chek qabul qilindi. Admin to'lovni tekshirgach, hisobingizga mablag' tushadi.")
    await message.answer("🏠 Bosh menyuga qaytdingiz.", reply_markup=main_menu_kb())
    await state.clear()

# Tranzaksiyalar tarixi
@router.message(F.text == "Tranzaksiyalar tarixi")
async def transaction_history(message: Message):
    transactions = await db.get_transactions(message.from_user.id)
    
    if not transactions:
        await message.answer("📊 Sizda hali tranzaksiyalar mavjud emas.")
        return
    
    text = "📊 **Tranzaksiyalar tarixi:**\n\n"
    
    for trans in transactions:
        date = trans.get('created_at', '')
        amount = trans.get('amount', 0)
        trans_type = trans.get('transaction_type', '')
        desc = trans.get('description', '')
        
        sign = "+" if amount > 0 else "-"
        date_str = str(date)[:19] if date else "Noma'lum"
        
        text += f"📅 {date_str}\n"
        text += f"💰 {sign}{abs(amount):,} so'm ({trans_type})\n"
        text += f"📝 {desc}\n\n"
    
    await message.answer(text[:4000])
