from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
import asyncio

from database import Database
from keyboards import main_menu_kb
from config import ADMIN_ID

router = Router()
db = Database()

# Botni global o'zgaruvchidan olish
from main import get_bot

# Admin ID ni tekshirish
def is_admin(user_id: int) -> bool:
    try:
        # Agar ADMIN_ID raqam bo'lsa
        if ADMIN_ID.isdigit():
            return str(user_id) == ADMIN_ID
        # Agar @ bilan boshlansa, boshqa usul
        else:
            # Bu yerda siz adminlarni bazada saqlashingiz kerak
            # Hozircha faqat bitta admin
            admin_ids = [int(ADMIN_ID.replace('@', '')) if ADMIN_ID.startswith('@') else int(ADMIN_ID)]
            return user_id in admin_ids
    except:
        return False

# Admin komandalari
@router.message(Command("admin"))
async def admin_panel(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("Siz admin emassiz!")
        return
    
    text = """🛠 **Admin paneli**

Quyidagi funksiyalardan birini tanlang:

1. /admin_users - Foydalanuvchilar ro'yxati
2. /admin_add_money <user_id> <summa> - Balans to'ldirish
3. /admin_profiles - Profillar ro'yxati
4. /admin_stats - Statistika
5. /admin_broadcast - Hammaga xabar yuborish
6. /admin_help - Yordam"""
    
    await message.answer(text)

# Foydalanuvchilar ro'yxati
@router.message(Command("admin_users"))
async def admin_users(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Siz admin emassiz!")
        return
    
    try:
        users = await db.get_all_users()
        
        if not users:
            await message.answer("Foydalanuvchilar topilmadi.")
            return
        
        text = "👥 **Oxirgi 30 ta foydalanuvchi:**\n\n"
        for user in users[:30]:
            text += f"🆔 ID: {user.get('user_id')}\n"
            text += f"👤 Ism: {user.get('first_name')}\n"
            text += f"🔗 Username: @{user.get('username') or 'Yo\\'q'}\n"
            text += f"📞 Tel: {user.get('phone') or 'Yo\\'q'}\n"
            text += f"💰 Balans: {user.get('balance', 0):,} so'm\n"
            text += f"📝 Profil: {'✅ To\\'ldirgan' if user.get('profile_completed') else '❌ To\\'ldirmagan'}\n"
            text += f"📅 Ro'yxatdan o'tgan: {str(user.get('created_at', ''))[:10]}\n"
            text += "─" * 30 + "\n"
        
        await message.answer(text[:4000])
    except Exception as e:
        await message.answer(f"Xatolik: {str(e)}")

# Balans to'ldirish
@router.message(Command("admin_add_money"))
async def admin_add_money(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Siz admin emassiz!")
        return
    
    args = message.text.split()
    if len(args) != 3:
        await message.answer("Xato format! Foydalanish: /admin_add_money <user_id> <summa>\nMasalan: /admin_add_money 123456789 50000")
        return
    
    try:
        user_id = int(args[1])
        amount = int(args[2])
    except ValueError:
        await message.answer("Xato! user_id va summa raqam bo'lishi kerak.")
        return
    
    # Foydalanuvchini tekshirish
    user = await db.get_user(user_id)
    if not user:
        await message.answer(f"Foydalanuvchi {user_id} topilmadi.")
        return
    
    # Balansni to'ldirish
    await db.update_balance(
        user_id=user_id,
        amount=amount,
        transaction_type="admin_add",
        description=f"Admin tomonidan qo'shildi"
    )
    
    # Yangi balans
    new_balance = await db.get_user_balance(user_id)
    
    text = f"""✅ **Balans to'ldirildi!**

👤 Foydalanuvchi: @{user.get('username') or user.get('first_name')}
🆔 ID: {user_id}
💰 Qo'shilgan summa: {amount:,} so'm
🏦 Yangi balans: {new_balance:,} so'm

💳 Admin: @{message.from_user.username}
⏰ Vaqt: {message.date.strftime('%H:%M:%S')}"""
    
    await message.answer(text)
    
    # Foydalanuvchiga xabar
    user_text = f"""💰 **Hisobingiz to'ldirildi!**

Summa: {amount:,} so'm
Yangi balans: {new_balance:,} so'm
Admin: @{message.from_user.username}

Rahmat! 😊"""
    
    try:
        bot = get_bot()
        await bot.send_message(chat_id=user_id, text=user_text)
    except Exception as e:
        await message.answer(f"⚠️ Foydalanuvchiga xabar yuborib bo'lmadi: {str(e)}")

# Yordam
@router.message(Command("admin_help"))
async def admin_help(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Siz admin emassiz!")
        return
    
    text = """🛠 **Admin paneli - Yordam**

**Komandalar:**
• /admin - Admin paneli
• /admin_users - Foydalanuvchilar ro'yxati
• /admin_add_money <id> <summa> - Balans to'ldirish
• /admin_profiles - Profillar ro'yxati
• /admin_stats - Statistika
• /admin_broadcast - Hammaga xabar

**Misol:**
/admin_add_money 123456789 50000
→ 123456789 ID li foydalanuvchiga 50,000 so'm qo'shadi

**Eslatma:** Faqat adminlar foydalana oladi."""
    
    await message.answer(text)

@router.message(Command("admin_stats"))
async def admin_stats(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Siz admin emassiz!")
        return
    
    try:
        # Umumiy foydalanuvchilar
        users = await db.get_all_users()
        total_users = len(users)
        
        # Profil to'ldirganlar
        profiles_filled = sum(1 for user in users if user.get('profile_completed'))
        
        # Umumiy balans
        total_balance = sum(user.get('balance', 0) for user in users)
        
        # Bugungi tranzaksiyalar
        today = message.date.strftime('%Y-%m-%d')
        
        text = f"""📊 **Bot statistikasi**

👥 **Foydalanuvchilar:**
• Umumiy: {total_users} ta
• Profil to'ldirgan: {profiles_filled} ta
• Profil to'ldirmagan: {total_users - profiles_filled} ta

💰 **Moliyaviy:**
• Umumiy balans: {total_balance:,} so'm

📅 **Sana:** {message.date.strftime('%Y-%m-%d %H:%M')}"""
        
        await message.answer(text)
    except Exception as e:
        await message.answer(f"Statistika olishda xatolik: {str(e)}")

# Simple broadcast
@router.message(Command("admin_broadcast"))
async def admin_broadcast(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("Siz admin emassiz!")
        return
    
    await message.answer("📢 Xabarni yuboring (matn):")
    await state.set_state("admin_broadcast_text")

@router.message(F.state == "admin_broadcast_text")
async def process_broadcast(message: Message, state: FSMContext):
    try:
        users = await db.get_all_users()
        total = len(users)
        
        await message.answer(f"📤 {total} ta foydalanuvchiga xabar yuborilmoqda...")
        
        bot = get_bot()
        success = 0
        
        for user in users:
            try:
                await bot.send_message(
                    chat_id=user.get('user_id'),
                    text=message.text
                )
                success += 1
                await asyncio.sleep(0.1)  # Rate limit uchun
            except:
                continue
        
        await message.answer(f"✅ {success}/{total} ta foydalanuvchiga xabar yuborildi.")
        await state.clear()
        
    except Exception as e:
        await message.answer(f"Xatolik: {str(e)}")
        await state.clear()
