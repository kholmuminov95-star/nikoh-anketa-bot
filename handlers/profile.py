from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database import Database
from states import ProfileStates
from keyboards import *
from utils import validate_age, validate_height, validate_weight, validate_languages, format_profile

router = Router()
db = Database()

# 1. Jinsni tanlash
@router.message(F.text.in_(["Erkak", "Ayol"]))
async def handle_gender(message: Message, state: FSMContext):
    gender = message.text
    await state.update_data(gender=gender)
    
    text = """Bu NIKOH platformasi. Anketani faqat valiyingiz (ota-ona, aka-uka) roziligi bilan to'ldiring.
Valiysiz e'lon berish dinimizga va odatimizga zid.
O'zingizga va boshqalarga zulm qilmang.

Profilni to'ldirish orqali siz maxfiy e'lon joylashtirasiz. Raqamingiz va username'ingiz faqat VIP a'zolarga ko'rsatilishi mumkun.

Yoshingizni kiriting (18-99):"""
    
    await message.answer(text)
    await state.set_state(ProfileStates.waiting_for_age)

# 2. Yoshni olish
@router.message(ProfileStates.waiting_for_age, F.text)
async def handle_age(message: Message, state: FSMContext):
    if message.text == "Bosh menyu":
        await main_menu(message, state)
        return
    
    age = validate_age(message.text)
    if not age:
        await message.answer("Iltimos, 18-99 oralig'ida bo'lgan yoshingizni kiriting:")
        return
    
    await state.update_data(age=age)
    await message.answer("Bo'yingizni kiriting (100-250 sm):")
    await state.set_state(ProfileStates.waiting_for_height)

# 3. Bo'y
@router.message(ProfileStates.waiting_for_height, F.text)
async def handle_height(message: Message, state: FSMContext):
    if message.text == "Bosh menyu":
        await main_menu(message, state)
        return
    
    height = validate_height(message.text)
    if not height:
        await message.answer("Bo'y 100-250 sm oralig'ida bo'lishi kerak:")
        return
    
    await state.update_data(height=height)
    await message.answer("Vazningizni kiriting (30-200 kg):")
    await state.set_state(ProfileStates.waiting_for_weight)

# 4. Vazn
@router.message(ProfileStates.waiting_for_weight, F.text)
async def handle_weight(message: Message, state: FSMContext):
    if message.text == "Bosh menyu":
        await main_menu(message, state)
        return
    
    weight = validate_weight(message.text)
    if not weight:
        await message.answer("Vazn 30-200 kg oralig'ida bo'lishi kerak:")
        return
    
    await state.update_data(weight=weight)
    await message.answer("Millatingizni tanlang:", reply_markup=nationality_kb())
    await state.set_state(ProfileStates.waiting_for_nationality)

# 5. Millat
@router.message(ProfileStates.waiting_for_nationality, F.text)
async def handle_nationality(message: Message, state: FSMContext):
    if message.text == "Bosh menyu":
        await main_menu(message, state)
        return
    
    if message.text == "Boshqa":
        await message.answer("Millatingizni kiriting:")
        await state.set_state(ProfileStates.waiting_for_nationality_custom)
        return
    
    await state.update_data(nationality=message.text)
    data = await state.get_data()
    
    if data['gender'] == "Erkak":
        await message.answer("Oilaviy holatingizni tanlang:", reply_markup=marital_status_male_kb())
        await state.set_state(ProfileStates.waiting_for_marital_status)
    else:
        await message.answer("Oilaviy holatingizni tanlang:", reply_markup=marital_status_female_kb())
        await state.set_state(ProfileStates.waiting_for_marital_status)

@router.message(ProfileStates.waiting_for_nationality_custom, F.text)
async def handle_nationality_custom(message: Message, state: FSMContext):
    if message.text == "Bosh menyu":
        await main_menu(message, state)
        return
    
    await state.update_data(nationality=message.text)
    data = await state.get_data()
    
    if data['gender'] == "Erkak":
        await message.answer("Oilaviy holatingizni tanlang:", reply_markup=marital_status_male_kb())
        await state.set_state(ProfileStates.waiting_for_marital_status)
    else:
        await message.answer("Oilaviy holatingizni tanlang:", reply_markup=marital_status_female_kb())
        await state.set_state(ProfileStates.waiting_for_marital_status)

# 6. Oilaviy holat
@router.message(ProfileStates.waiting_for_marital_status, F.text)
async def handle_marital_status(message: Message, state: FSMContext):
    if message.text == "Bosh menyu":
        await main_menu(message, state)
        return
    
    await state.update_data(marital_status=message.text)
    data = await state.get_data()
    
    # Agar ajrashgan yoki beva bo'lsa, farzandlar sonini so'rash
    if message.text in ['Ajrashgan', 'Beva']:
        await message.answer("Farzandlaringiz sonini kiriting (0-10, yo'q bo'lsa 0):")
        await state.set_state(ProfileStates.waiting_for_children)
    else:
        await state.update_data(children=0)
        await ask_country(message, state)

async def ask_country(message: Message, state: FSMContext):
    data = await state.get_data()
    
    if data['gender'] == "Ayol":
        await message.answer("Ro'mol o'raysizmi?", reply_markup=yes_no_kb())
        await state.set_state(ProfileStates.waiting_for_hijab)
    else:
        await message.answer("Manzilingizni tanlang:", reply_markup=countries_kb())
        await state.set_state(ProfileStates.waiting_for_country)

# 7. Farzandlar
@router.message(ProfileStates.waiting_for_children, F.text)
async def handle_children(message: Message, state: FSMContext):
    if message.text == "Bosh menyu":
        await main_menu(message, state)
        return
    
    try:
        children = int(message.text)
        if 0 <= children <= 10:
            await state.update_data(children=children)
            data = await state.get_data()
            
            if data['gender'] == "Ayol":
                await message.answer("Ro'mol o'raysizmi?", reply_markup=yes_no_kb())
                await state.set_state(ProfileStates.waiting_for_hijab)
            else:
                await message.answer("Manzilingizni tanlang:", reply_markup=countries_kb())
                await state.set_state(ProfileStates.waiting_for_country)
        else:
            await message.answer("Farzandlar soni 0-10 oralig'ida bo'lishi kerak:")
    except:
        await message.answer("Iltimos, raqam kiriting (0-10):")

# 8. Ro'mol (faqat ayollar)
@router.message(ProfileStates.waiting_for_hijab, F.text)
async def handle_hijab(message: Message, state: FSMContext):
    if message.text == "Bosh menyu":
        await main_menu(message, state)
        return
    
    hijab = message.text == "Ha"
    await state.update_data(hijab=hijab)
    await message.answer("Ko'chib o'tishga tayyormisiz?", reply_markup=yes_no_kb())
    await state.set_state(ProfileStates.waiting_for_ready_to_move)

# 9. Ko'chish (faqat ayollar)
@router.message(ProfileStates.waiting_for_ready_to_move, F.text)
async def handle_ready_to_move(message: Message, state: FSMContext):
    if message.text == "Bosh menyu":
        await main_menu(message, state)
        return
    
    ready = message.text == "Ha"
    await state.update_data(ready_to_move=ready)
    await message.answer("2-likka rozimisiz?", reply_markup=second_wife_kb())
    await state.set_state(ProfileStates.waiting_for_second_wife)

# 10. Ikkinchi xotin (faqat ayollar)
@router.message(ProfileStates.waiting_for_second_wife, F.text)
async def handle_second_wife(message: Message, state: FSMContext):
    if message.text == "Bosh menyu":
        await main_menu(message, state)
        return
    
    await state.update_data(ready_for_second_wife=message.text)
    await message.answer("Manzilingizni tanlang:", reply_markup=countries_kb())
    await state.set_state(ProfileStates.waiting_for_country)

# 11. Mamlakat
@router.message(ProfileStates.waiting_for_country, F.text)
async def handle_country(message: Message, state: FSMContext):
    if message.text == "Bosh menyu":
        await main_menu(message, state)
        return
    
    await state.update_data(country=message.text)
    
    if message.text == "O'zbekiston":
        await message.answer("Viloyatni tanlang:", reply_markup=regions_kb())
        await state.set_state(ProfileStates.waiting_for_region)
    else:
        await message.answer("Asli qayerliksiz?", reply_markup=countries_kb())
        await state.set_state(ProfileStates.waiting_for_origin_country)

# 12. Viloyat (O'zbekiston uchun)
@router.message(ProfileStates.waiting_for_region, F.text)
async def handle_region(message: Message, state: FSMContext):
    if message.text == "Bosh menyu":
        await main_menu(message, state)
        return
    
    await state.update_data(region=message.text)
    await message.answer("Asli qayerliksiz?", reply_markup=countries_kb())
    await state.set_state(ProfileStates.waiting_for_origin_country)

# 13. Asli mamlakat
@router.message(ProfileStates.waiting_for_origin_country, F.text)
async def handle_origin_country(message: Message, state: FSMContext):
    if message.text == "Bosh menyu":
        await main_menu(message, state)
        return
    
    await state.update_data(origin_country=message.text)
    
    if message.text == "O'zbekiston":
        await message.answer("Viloyatni tanlang:", reply_markup=regions_kb())
        await state.set_state(ProfileStates.waiting_for_origin_region)
    else:
        await message.answer("Namoz va Qur'on o'qiysizmi?", reply_markup=yes_no_kb())
        await state.set_state(ProfileStates.waiting_for_prays)

# 14. Asli viloyat
@router.message(ProfileStates.waiting_for_origin_region, F.text)
async def handle_origin_region(message: Message, state: FSMContext):
    if message.text == "Bosh menyu":
        await main_menu(message, state)
        return
    
    await state.update_data(origin_region=message.text)
    await message.answer("Namoz va Qur'on o'qiysizmi?", reply_markup=yes_no_kb())
    await state.set_state(ProfileStates.waiting_for_prays)

# 15. Namoz
@router.message(ProfileStates.waiting_for_prays, F.text)
async def handle_prays(message: Message, state: FSMContext):
    if message.text == "Bosh menyu":
        await main_menu(message, state)
        return
    
    prays = message.text == "Ha"
    await state.update_data(prays=prays)
    await message.answer("Nechta til bilasiz? (1-10):")
    await state.set_state(ProfileStates.waiting_for_languages)

# 16. Tillar
@router.message(ProfileStates.waiting_for_languages, F.text)
async def handle_languages(message: Message, state: FSMContext):
    if message.text == "Bosh menyu":
        await main_menu(message, state)
        return
    
    languages = validate_languages(message.text)
    if not languages:
        await message.answer("Iltimos, 1-10 oralig'ida bo'lgan til sonini kiriting:")
        return
    
    await state.update_data(languages=languages)
    await message.answer("O'zingiz haqingizda yozing: (ko'rinishiz, harakteriz, nimalarga qiziqasiz?)")
    await state.set_state(ProfileStates.waiting_for_about)

# 17. O'zi haqida
@router.message(ProfileStates.waiting_for_about, F.text)
async def handle_about(message: Message, state: FSMContext):
    if message.text == "Bosh menyu":
        await main_menu(message, state)
        return
    
    await state.update_data(about=message.text)
    
    data = await state.get_data()
    if data['gender'] == "Erkak":
        await message.answer("Kelin uchun talablar: (javob text shaklida)")
    else:
        await message.answer("Kuyov uchun talablar: (javob text shaklida)")
    
    await state.set_state(ProfileStates.waiting_for_requirements)

# 18. Talablar
@router.message(ProfileStates.waiting_for_requirements, F.text)
async def handle_requirements(message: Message, state: FSMContext):
    if message.text == "Bosh menyu":
        await main_menu(message, state)
        return
    
    await state.update_data(requirements=message.text)
    await message.answer("Anketani kim to'ldirdi?", reply_markup=filled_by_kb())
    await state.set_state(ProfileStates.waiting_for_filled_by)

# 19. Kim to'ldirdi
@router.message(ProfileStates.waiting_for_filled_by, F.text)
async def handle_filled_by(message: Message, state: FSMContext):
    if message.text == "Bosh menyu":
        await main_menu(message, state)
        return
    
    await state.update_data(filled_by=message.text)
    
    # Tasdiqlash uchun anketani ko'rsatish
    data = await state.get_data()
    profile_text = format_profile(data, data['gender'])
    
    await message.answer(profile_text, reply_markup=retry_kb())
    await state.set_state(ProfileStates.confirming_profile)

# 20. Tasdiqlash
@router.callback_query(ProfileStates.confirming_profile, F.data == "confirm")
async def confirm_profile(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    
    # Profilni saqlash
    profile_id = await db.create_profile(callback.from_user.id, **data)
    
    # Foydalanuvchi ma'lumotlarini yangilash
    await db.update_user_profile(callback.from_user.id, **data)
    
    # Tasdiqlash xabari
    if data['gender'] == "Erkak":
        text = """Erkaklar bilan gaplashish tartibi
        1. Ayollar siz joylashtirgan e'lon (anketa)ga qiziqish bildirsa, bot orqali so'rov yuborishadi.
        2. Sizga so'rov kelganida, ayolning qisqacha ma'lumotlarini ko'rasiz va qabul qilish yoki rad etish imkoniyatiga ega bo'lasiz.
        3. Agar siz 24 soat ichida javob bermasangiz, so'rov avtomatik tarzda bekor qilinadi.
        4. Agar siz so'rovni qabul qilsangiz, siz va ayol o'rtasida chat oynasi ochiladi.
        5. Chatga kirish uchun ?? Chatlarim bo'limiga kirib, kerakli anketa raqamini tanlang.
        6. Endi ayol sizga xabar yozishi mumkin. Siz ham javob bera olasiz.
        7. Yozishmalar saqlanadi va admin tomonidan nazorat qilinadi.
        • Iltimos, hurmat va hayo doirasida muloqot qiling.
        8. Agar sizga u inson ma'qul bo'lsa, "Lichkani ochish" taklifini qabul qilishingiz mumkin.
        • Chat orqali bevosita lichkangizni bermang!
        9. Agar fikrlaringiz mos kelmasa, "Chatni tugatish" tugmasi orqali muloqotni yakunlashingiz mumkin."""
    else:
        text = """Ayollar bilan gaplashish tartibi
        1. Erkaklar siz joylashtirgan e'lon (anketa)ga qiziqish bildirsa, bot orqali so'rov yuborishadi.
        2. Sizga so'rov kelganida, erkakning qisqacha ma'lumotlarini ko'rasiz va qabul qilish yoki rad etish imkoniyatiga ega bo'lasiz.
        3. Agar siz 24 soat ichida javob bermasangiz, so'rov avtomatik tarzda bekor qilinadi.
        4. Agar siz so'rovni qabul qilsangiz, siz va erkak o'rtasida chat oynasi ochiladi.
        5. Chatga kirish uchun ?? Chatlarim bo'limiga kirib, kerakli anketa raqamini tanlang.
        6. Endi erkak sizga xabar yozishi mumkin. Siz ham javob bera olasiz.
        7. Yozishmalar saqlanadi va admin tomonidan nazorat qilinadi.
        • Iltimos, hurmat va hayo doirasida muloqot qiling.
        8. Agar sizga u inson ma'qul bo'lsa, "Lichkani ochish" taklifini qabul qilishingiz mumkin.
        • Chat orqali bevosita lichkangizni bermang!
        9. Agar fikrlaringiz mos kelmasa, "Chatni tugatish" tugmasi orqali muloqotni yakunlashingiz mumkin.
        
        ?? Eslatma: Nomzodlar sizga yoza olishi uchun sozlamalaringizni shunday ko'rinishga keltiring Sozlamalar -> Foydalanuvchi nomi -> zuhra1608 (hohlagan nom qo'yasiz) (Agar qanday qilishni tushunmagan bo'lsangiz, ushbu rasmga qarang: ?? https://t.me/nikohboti/8)"""
    
    await callback.message.answer(text)
    
    text2 = """? Profilingiz saqlandi va maxfiy anketalar bo'limiga qo'shildi! Hozirda profilingizni faqat VIP A'zolar ko'ra oladi. Agar @Nikoh_01 kanaliga e'lon berishni istasangiz, Bosh menyudan ?? E'lon joylashtirish tugmasi orqali e'lon bera olasiz (@nikohboti kanalida video qilib ko'rsatilgan)"""
    
    await callback.message.answer(text2, reply_markup=main_menu_kb())
    await state.clear()

@router.callback_query(ProfileStates.confirming_profile, F.data == "retry")
async def retry_profile(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Jinsingizni tanlang:", reply_markup=gender_kb())
    await state.set_state(ProfileStates.waiting_for_gender)

@router.callback_query(ProfileStates.confirming_profile, F.data == "main_menu")
async def profile_to_main_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Bosh menyuga qaytdingiz.", reply_markup=main_menu_kb())
    await state.clear()
