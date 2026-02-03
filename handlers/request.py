from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database import Database
from states import RequestStates, AdStates
from keyboards import *

router = Router()
db = Database()

async def main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("🏠 Bosh menyuga qaytdingiz.", reply_markup=main_menu_kb())

# So'rov yuborish boshlash
@router.message(F.text == "So'rov yuborish")
async def request_start(message: Message, state: FSMContext):
    await message.answer("🔍 Anketa raqamini kiriting: (Anketa raqami @Hayrli_nikoh_kanali kanalidan olinadi)")
    await state.set_state(RequestStates.waiting_for_profile_id)

@router.message(RequestStates.waiting_for_profile_id, F.text)
async def handle_profile_id(message: Message, state: FSMContext):
    if message.text == "Bosh menyu":
        await main_menu(message, state)
        return
    
    try:
        profile_id = int(message.text)
        
        # Mock profil ma'lumotlari (keyin bazaga ulaysiz)
        profile_data = {
            "profile_id": profile_id,
            "age": 31,
            "height": 169,
            "weight": 55,
            "nationality": "O'zbek",
            "marital_status": "Ajrashgan",
            "children": 2,
            "country": "O'zbekiston",
            "origin_country": "Toshkent",
            "prays": True,
            "languages": 2,
            "ready_to_move": True,
            "about": "O'ranganman. Alhamdulillah Alloh bergan husnim bor shoh erkarogman. 2-likka o'ylab ko'riladi.",
            "requirements": "Shahsida gaplashamiz",
            "gender": "Ayol"
        }
        
        # Jinsni tekshirish (keyin bazadan olasiz)
        user = await db.get_user(message.from_user.id)
        if user and user.get('gender') == profile_data['gender']:
            await message.answer("⚠️ Siz faqat qarama-qarshi jinsdagi foydalanuvchilarga so'rov yuborishingiz mumkin.")
            await main_menu(message, state)
            return
        
        from utils import format_profile
        text = format_profile(profile_data, profile_data['gender'])
        
        await message.answer(text, reply_markup=send_request_kb(profile_id))
        await state.set_state(RequestStates.confirming_request)
        await state.update_data(profile_id=profile_id)
        
    except ValueError:
        await message.answer("⚠️ Iltimos, anketa raqamini to'g'ri kiriting:")

# E'lon joylashtirish
@router.message(F.text == "E'lon joylashtirish")
async def ad_start(message: Message, state: FSMContext):
    text = "📢 **E'lon joylashtirish turini tanlang:**"
    await message.answer(text, reply_markup=ad_types_kb())
    await state.set_state(AdStates.waiting_for_ad_type)

@router.message(AdStates.waiting_for_ad_type, F.text == "Oddiy e'lon joylashtirish")
async def normal_ad(message: Message, state: FSMContext):
    user_profile = await db.get_user_profile(message.from_user.id)
    
    if not user_profile:
        await message.answer("⚠️ Avval profilingizni to'ldiring.")
        await main_menu(message, state)
        return
    
    text = """📋 **Oddiy e'lon:**

ℹ️ Bu e'lon 2-7 kun ichida umumiy kanalda navbat asosida joylashtiriladi. 
Nomzodlar sizga shaxsiydan ham, bot orqali ham so'rov yuborib yoza oladilar.

⚠️ Agar 'username'ingizni o'zgartirsangiz yoki o'chirsangiz berilgan e'lon bekor qilindi deb hisoblanadi va kanalga joylanmaydi.

💵 Narxi: Bepul (har 15 kunda bir marta yangilasa bo'ladi)

⏰ Tasdiqlashdan 2-3 kundan so'ng @hayrli_nikoh_admin ga yozib eslatib qo'ying!

(Agar Tezkor e'lon berishni istasangiz "Tezkor e'lon joylashtirish" ni tanlang eloningiz (to'lov evaziga) 24 soat ichida kanalga joylashtiriladi."""
    
    await message.answer(text)
    
    from utils import format_profile
    profile_text = format_profile(user_profile, user_profile.get('gender'))
    await message.answer(profile_text)
    
    text2 = """📨 **E'lon so'rovi yuborish:**

📋 E'lon turi: Oddiy
💰 Hisobingizdan 0 so'm yechiladi.

⚠️ E'lon tasdiqlangach, uni o'zgartirish yoki orqaga qaytarish mumkin emas.
❌ Bekor qilingan e'lon qayta tiklanmaydi va puli qaytarilmaydi.

✅ Shunga rozimisiz? Tasdiqlaysizmi?"""
    
    await message.answer(text2, reply_markup=confirm_kb())
    await state.set_state(AdStates.confirming_ad)

@router.callback_query(AdStates.confirming_ad, F.data == "confirm")
async def confirm_ad(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("✅ E'lon so'rovi yuborildi! Admin e'lonni tekshirgach, kanalga joylashtiradi.")
    await callback.message.answer("🏠 Bosh menyuga qaytdingiz.", reply_markup=main_menu_kb())
    await state.clear()

@router.callback_query(AdStates.confirming_ad, F.data == "cancel")
async def cancel_ad(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("❌ E'lon joylashtirish bekor qilindi.")
    await callback.message.answer("🏠 Bosh menyuga qaytdingiz.", reply_markup=main_menu_kb())
    await state.clear()
