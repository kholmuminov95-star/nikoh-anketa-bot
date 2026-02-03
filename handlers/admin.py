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

# Admin ID ni tekshirish
def is_admin(user_id: int) -> bool:
    try:
        admin_id = ADMIN_ID.replace('@', '')
        return str(user_id) == admin_id
    except:
        return False

# Admin paneli
@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⚠️ Siz admin emassiz!")
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
        await message.answer("⚠️ Siz admin emassiz!")
        return
    
    try:
        users = await db.get_all_users()
        
        if not users:
            await message.answer("👥 Foydalanuvchilar topilmadi.")
            return
        
        text = "👥 **Oxirgi 30 ta foydalanuvchi:**\n\n"
        for user in users[:30]:
            username = user.get('username', 'Yoq')
            phone = user.get('phone', 'Yoq')
            
            text += f"🆔 ID: {user.get('user_id')}\n"
            text += f"👤 Ism: {user.get('first_name')}\n"
            text += f"🔗 Username: @{username}\n"
            text += f"📞 Tel: {phone}\n"
            text += f"💰 Balans: {user.get('balance', 0):,} so'm\n"
            
            profile_status = "To'ldirgan" if user.get('profile_completed') else "To'ldirmagan"
            text += f"📝 Profil: {profile_status}\n"
            
            created_at = str(user.get('created_at', ''))[:10]
            text += f"📅 Ro'yxatdan o'tgan: {created_at}\n"
            text += "─" * 30 + "\n"
        
        await message.answer(text[:4000])
    except Exception as e:
        await message.answer(f"❌ Xatolik: {str(e)}")

# Balans to'ldirish
@router.message(Command("admin_add_money"))
async def admin_add_money(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⚠️ Siz admin emassiz!")
        return
    
    args = message.text.split()
    if len(args) != 3:
        await message.answer("❌ Xato format! Foydalanish: /admin_add_money <user_id> <summa>\nMasalan: /admin_add_money 123456789 50000")
        return
    
    try:
        user_id = int(args[1])
        amount = int(args[2])
    except ValueError:
        await message.answer("❌ Xato! user_id va summa raqam bo'lishi kerak.")
        return
    
    user = await db.get_user(user_id)
    if not user:
        await message.answer(f"❌ Foydalanuvchi {user_id} topilmadi.")
        return
    
    await db.update_balance(
        user_id=user_id,
        amount=amount,
        transaction_type="admin_add",
        description=f"Admin tomonidan qo'shildi"
    )
    
    new_balance = await db.get_user_balance(user_id)
    
    username = user.get('username') or user.get('first_name')
    admin_username = message.from_user.username or "Admin"
    
    text = f"""✅ **Balans to'ldirildi!**

👤 Foydalanuvchi: @{username}
🆔 ID: {user_id}
💰 Qo'shilgan summa: {amount:,} so'm
🏦 Yangi balans: {new_balance:,} so'm

💳 Admin: @{admin_username}
⏰ Vaqt: {message.date.strftime('%H:%M:%S')}"""
    
    await message.answer(text)

# Yordam
@router.message(Command("admin_help"))
async def admin_help(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⚠️ Siz admin emassiz!")
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

# Statistika
@router.message(Command("admin_stats"))
async def admin_stats(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⚠️ Siz admin emassiz!")
        return
    
    try:
        users = await db.get_all_users()
        total_users = len(users)
        
        profiles_filled = sum(1 for user in users if user.get('profile_completed'))
        total_balance = sum(user.get('balance', 0) for user in users)
        
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
        await message.answer(f"❌ Statistika olishda xatolik: {str(e)}")

# Profillar ro'yxati
@router.message(Command("admin_profiles"))
async def admin_profiles(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("⚠️ Siz admin emassiz!")
        return
    
    try:
        profiles = await db.get_all_profiles()
        
        if not profiles:
            await message.answer("📋 Profil topilmadi.")
            return
        
        text = "📋 **Oxirgi 20 ta profil:**\n\n"
        for profile in profiles[:20]:
            text += f"🆔 Profil ID: #{profile.get('profile_id')}\n"
            text += f"👤 User ID: {profile.get('user_id')}\n"
            text += f"⚤ Jins: {profile.get('gender')}\n"
            text += f"🎂 Yosh: {profile.get('age')}\n"
            text += f"📅 Sana: {str(profile.get('created_at', ''))[:10]}\n"
            status = "Public" if profile.get('is_public') else "Private"
            text += f"📊 Status: {status}\n"
            text += "─" * 30 + "\n"
        
        await message.answer(text[:4000])
    except Exception as e:
        await message.answer(f"❌ Xatolik: {str(e)}")

# Simple broadcast
@router.message(Command("admin_broadcast"))
async def admin_broadcast(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("⚠️ Siz admin emassiz!")
        return
    
    await message.answer("📢 Xabarni yuboring (matn):")
    await state.set_state("admin_broadcast_text")

@router.message(F.state == "admin_broadcast_text")
async def process_broadcast(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("⚠️ Siz admin emassiz!")
        return
    
    try:
        await message.answer("📤 Xabar yuborish boshlandi...")
        await state.clear()
        await message.answer("✅ Xabar yuborish sozlamalari saqlandi.")
        
    except Exception as e:
        await message.answer(f"❌ Xatolik: {str(e)}")
        await state.clear()
