from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from database import Database
from keyboards import main_menu_kb, confirm_kb
from config import ADMIN_ID

router = Router()
db = Database()

# Admin ID ni tekshirish
def is_admin(user_id: int) -> bool:
    # ADMIN_ID @ bilan boshlansa, raqamli ID ga o'zgartirish kerak
    # Bu yerda siz admin ID ni bazada saqlashingiz yoki config dan olishingiz mumkin
    try:
        return str(user_id) == ADMIN_ID.replace('@', '')
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
2. /admin_balance <user_id> <summa> - Balans to'ldirish
3. /admin_profiles - Profillar ro'yxati
4. /admin_requests - So'rovlar ro'yxati
5. /admin_ads - E'lonlarni tasdiqlash
6. /admin_stats - Statistika
7. /admin_broadcast - Hammaga xabar yuborish"""
    
    await message.answer(text)

# 1. Foydalanuvchilar ro'yxati
@router.message(Command("admin_users"))
async def admin_users(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Siz admin emassiz!")
        return
    
    # Barcha foydalanuvchilarni olish
    async with db.connection() as conn:
        cursor = await conn.execute('''
            SELECT user_id, phone, first_name, username, balance, profile_completed, created_at 
            FROM users 
            ORDER BY created_at DESC 
            LIMIT 50
        ''')
        users = await cursor.fetchall()
    
    if not users:
        await message.answer("Foydalanuvchilar topilmadi.")
        return
    
    text = "👥 **Foydalanuvchilar ro'yxati:**\n\n"
    for user in users:
        text += f"🆔 ID: {user[0]}\n"
        text += f"📞 Tel: {user[1] or 'Yo'q'}\n"
        text += f"👤 Ism: {user[2]}\n"
        text += f"🔗 Username: @{user[3] or 'Yo'q'}\n"
        text += f"💰 Balans: {user[4]:,} so'm\n"
        text += f"📝 Profil: {'✅ To\'ldirgan' if user[5] else '❌ To\'ldirmagan'}\n"
        text += f"📅 Ro'yxatdan o'tgan: {user[6][:10]}\n"
        text += "─" * 30 + "\n"
    
    await message.answer(text[:4000])  # Telegram limiti

# 2. Balans to'ldirish
@router.message(Command("admin_balance"))
async def admin_balance_command(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Siz admin emassiz!")
        return
    
    args = message.text.split()
    if len(args) != 3:
        await message.answer("Xato format! Foydalanish: /admin_balance <user_id> <summa>")
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
        transaction_type="admin_deposit",
        description=f"Admin tomonidan to'ldirildi. Admin: @{message.from_user.username}"
    )
    
    # Yangi balans
    new_balance = await db.get_user_balance(user_id)
    
    text = f"""✅ **Balans to'ldirildi!**

👤 Foydalanuvchi: @{user.get('username') or user.get('first_name')}
🆔 ID: {user_id}
💰 Qo'shilgan summa: {amount:,} so'm
🏦 Yangi balans: {new_balance:,} so'm

💳 To'lov ma'lumotlari:
Admin: @{message.from_user.username}
Vaqt: {message.date}"""
    
    await message.answer(text)
    
    # Foydalanuvchiga xabar
    user_text = f"""💰 **Hisobingiz to'ldirildi!**

Summa: {amount:,} so'm
Yangi balans: {new_balance:,} so'm
Admin: @{message.from_user.username}

Rahmat! 😊"""
    
    from main import bot
    try:
        await bot.send_message(chat_id=user_id, text=user_text)
    except:
        await message.answer(f"⚠️ Foydalanuvchiga xabar yuborib bo'lmadi. ID: {user_id}")

# 3. Profillar ro'yxati
@router.message(Command("admin_profiles"))
async def admin_profiles(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Siz admin emassiz!")
        return
    
    async with db.connection() as conn:
        cursor = await conn.execute('''
            SELECT p.*, u.phone, u.username 
            FROM profiles p
            LEFT JOIN users u ON p.user_id = u.user_id
            ORDER BY p.created_at DESC 
            LIMIT 20
        ''')
        profiles = await cursor.fetchall()
    
    if not profiles:
        await message.answer("Profil topilmadi.")
        return
    
    text = "📋 **Oxirgi 20 ta profil:**\n\n"
    for profile in profiles:
        text += f"🆔 Profil ID: #{profile[0]}\n"
        text += f"👤 User ID: {profile[1]}\n"
        text += f"📞 Tel: {profile[24] or 'Yo'q'}\n"
        text += f"🔗 Username: @{profile[25] or 'Yo'q'}\n"
        text += f"⚤ Jins: {profile[2]}\n"
        text += f"🎂 Yosh: {profile[3]}\n"
        text += f"📅 Sana: {profile[22][:10]}\n"
        text += f"📊 Status: {'✅ Public' if profile[21] else '❌ Private'}\n"
        text += "─" * 30 + "\n"
    
    await message.answer(text[:4000])

# 4. So'rovlar ro'yxati
@router.message(Command("admin_requests"))
async def admin_requests(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Siz admin emassiz!")
        return
    
    async with db.connection() as conn:
        cursor = await conn.execute('''
            SELECT r.*, u1.username as from_user, u2.username as to_user
            FROM requests r
            LEFT JOIN users u1 ON r.from_user_id = u1.user_id
            LEFT JOIN profiles p ON r.to_profile_id = p.profile_id
            LEFT JOIN users u2 ON p.user_id = u2.user_id
            WHERE r.status = 'pending'
            ORDER BY r.created_at DESC
        ''')
        requests = await cursor.fetchall()
    
    if not requests:
        await message.answer("Kutilayotgan so'rovlar yo'q.")
        return
    
    text = "📨 **Kutilayotgan so'rovlar:**\n\n"
    for req in requests:
        text += f"🆔 So'rov ID: #{req[0]}\n"
        text += f"👤 Kimdan: @{req[7] or 'Yo'q'} (ID: {req[1]})\n"
        text += f"👥 Kimga: @{req[8] or 'Yo'q'} (Profil: #{req[2]})\n"
        text += f"💰 To'langan: {req[3]:,} so'm\n"
        text += f"📊 Status: {req[4]}\n"
        text += f"📅 Vaqt: {req[5][:19]}\n"
        text += "─" * 30 + "\n"
    
    await message.answer(text[:4000])

# 5. E'lonlarni tasdiqlash
@router.message(Command("admin_ads"))
async def admin_ads(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Siz admin emassiz!")
        return
    
    text = """📢 **E'lonlarni boshqarish**

Quyidagi komandalardan foydalaning:

1. /admin_ads_pending - Tasdiqlanishi kerak bo'lgan e'lonlar
2. /admin_ad_approve <profile_id> - E'lonni tasdiqlash
3. /admin_ad_reject <profile_id> - E'lonni rad etish
4. /admin_ads_active - Faol e'lonlar"""
    
    await message.answer(text)

# 5.1 Kutilayotgan e'lonlar
@router.message(Command("admin_ads_pending"))
async def admin_ads_pending(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Siz admin emassiz!")
        return
    
    async with db.connection() as conn:
        cursor = await conn.execute('''
            SELECT p.*, u.username, u.phone
            FROM profiles p
            LEFT JOIN users u ON p.user_id = u.user_id
            WHERE p.is_public = FALSE AND p.is_vip_only = FALSE
            ORDER BY p.created_at DESC
        ''')
        profiles = await cursor.fetchall()
    
    if not profiles:
        await message.answer("Kutilayotgan e'lonlar yo'q.")
        return
    
    text = "⏳ **Kutilayotgan e'lonlar:**\n\n"
    for profile in profiles:
        text += f"🆔 Profil ID: #{profile[0]}\n"
        text += f"👤 Username: @{profile[24] or 'Yo'q'}\n"
        text += f"📞 Tel: {profile[25] or 'Yo'q'}\n"
        text += f"⚤ Jins: {profile[2]}\n"
        text += f"🎂 Yosh: {profile[3]}\n"
        text += f"📅 Qo'shilgan: {profile[22][:10]}\n"
        text += f"✅ Tasdiqlash: /admin_ad_approve_{profile[0]}\n"
        text += f"❌ Rad etish: /admin_ad_reject_{profile[0]}\n"
        text += "─" * 30 + "\n"
    
    await message.answer(text[:4000])

# 5.2 E'lonni tasdiqlash
@router.message(F.text.startswith("/admin_ad_approve_"))
async def admin_ad_approve(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Siz admin emassiz!")
        return
    
    try:
        profile_id = int(message.text.split("_")[-1])
    except:
        await message.answer("Xato format!")
        return
    
    # Profilni public qilish
    async with db.connection() as conn:
        await conn.execute('UPDATE profiles SET is_public = TRUE WHERE profile_id = ?', (profile_id,))
        await conn.commit()
    
    # Profil ma'lumotlarini olish
    async with db.connection() as conn:
        cursor = await conn.execute('SELECT * FROM profiles WHERE profile_id = ?', (profile_id,))
        profile = await cursor.fetchone()
        
        if profile:
            cursor2 = await conn.execute('SELECT user_id, username FROM users WHERE user_id = ?', (profile[1],))
            user = await cursor2.fetchone()
    
    text = f"✅ Profil #{profile_id} kanalga joylash uchun tasdiqlandi!"
    await message.answer(text)
    
    # Foydalanuvchiga xabar
    if user:
        user_text = f"""🎉 Tabriklaymiz!

Sizning profilingiz (#{profile_id}) tasdiqlandi va @Nikoh_01 kanaliga joylashtirildi.

✅ Endi sizga so'rovlar kelishi mumkin.
✅ Profilingizni bosh menyudan ko'rishingiz mumkin.

Rahmat! 😊"""
        
        from main import bot
        try:
            await bot.send_message(chat_id=user[0], text=user_text)
        except:
            pass

# 6. Statistika
@router.message(Command("admin_stats"))
async def admin_stats(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Siz admin emassiz!")
        return
    
    async with db.connection() as conn:
        # Umumiy foydalanuvchilar
        cursor = await conn.execute('SELECT COUNT(*) FROM users')
        total_users = (await cursor.fetchone())[0]
        
        # Faol foydalanuvchilar (oxirgi 7 kun)
        cursor = await conn.execute('SELECT COUNT(DISTINCT user_id) FROM transactions WHERE created_at > datetime("now", "-7 days")')
        active_users = (await cursor.fetchone())[0]
        
        # Profil to'ldirganlar
        cursor = await conn.execute('SELECT COUNT(*) FROM users WHERE profile_completed = TRUE')
        profiles_filled = (await cursor.fetchone())[0]
        
        # Erkak/Ayol
        cursor = await conn.execute('SELECT gender, COUNT(*) FROM profiles GROUP BY gender')
        gender_stats = await cursor.fetchall()
        
        # Umumiy balans
        cursor = await conn.execute('SELECT SUM(balance) FROM users')
        total_balance = (await cursor.fetchone())[0] or 0
        
        # So'rovlar
        cursor = await conn.execute('SELECT status, COUNT(*) FROM requests GROUP BY status')
        request_stats = await cursor.fetchall()
        
        # Tranzaksiyalar (oxirgi 24 soat)
        cursor = await conn.execute('SELECT SUM(amount) FROM transactions WHERE created_at > datetime("now", "-1 day") AND amount > 0')
        daily_income = (await cursor.fetchone())[0] or 0
    
    text = f"""📊 **Bot statistikasi**

👥 **Foydalanuvchilar:**
• Umumiy: {total_users} ta
• Faol (7 kun): {active_users} ta
• Profil to'ldirgan: {profiles_filled} ta

⚤ **Jinslar bo'yicha:**
{format_gender_stats(gender_stats)}

💰 **Moliyaviy:**
• Umumiy balans: {total_balance:,} so'm
• Kunlik daromad: {daily_income:,} so'm

📨 **So'rovlar:**
{format_request_stats(request_stats)}

🕒 **Oxirgi yangilanish:** {message.date}"""
    
    await message.answer(text)

def format_gender_stats(stats):
    text = ""
    for gender, count in stats:
        text += f"• {gender}: {count} ta\n"
    return text

def format_request_stats(stats):
    text = ""
    for status, count in stats:
        status_text = {
            'pending': '⏳ Kutilmoqda',
            'accepted': '✅ Qabul qilingan',
            'rejected': '❌ Rad etilgan',
            'expired': '⌛️ Muddati o'tgan'
        }.get(status, status)
        text += f"• {status_text}: {count} ta\n"
    return text

# 7. Hammaga xabar yuborish
@router.message(Command("admin_broadcast"))
async def admin_broadcast_start(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("Siz admin emassiz!")
        return
    
    await message.answer("📢 **Hammaga xabar yuborish**\n\nXabarni yuboring (rasm, video yoki matn):")
    await state.set_state("admin_broadcast")

@router.message(F.state == "admin_broadcast")
async def admin_broadcast_send(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("Siz admin emassiz!")
        return
    
    # Barcha foydalanuvchilarni olish
    async with db.connection() as conn:
        cursor = await conn.execute('SELECT user_id FROM users')
        users = await cursor.fetchall()
    
    total = len(users)
    success = 0
    failed = 0
    
    await message.answer(f"📤 Xabar {total} ta foydalanuvchiga yuborilmoqda...")
    
    from main import bot
    for user in users:
        user_id = user[0]
        try:
            # Xabarni nusxalash
            if message.text:
                await bot.send_message(chat_id=user_id, text=message.text)
            elif message.photo:
                await bot.send_photo(chat_id=user_id, photo=message.photo[-1].file_id, caption=message.caption)
            elif message.video:
                await bot.send_video(chat_id=user_id, video=message.video.file_id, caption=message.caption)
            success += 1
        except Exception as e:
            failed += 1
            print(f"Xatolik {user_id}: {e}")
    
    await message.answer(f"""✅ **Xabar yuborish yakunlandi:**

👥 Jami: {total} ta
✅ Muvaffaqiyatli: {success} ta
❌ Xatolik: {failed} ta

Xabar {message.date} da yuborildi.""")
    
    await state.clear()

# Admin tomonidan chekni tasdiqlash
@router.message(F.photo, F.caption.contains("chek"))
async def admin_check_photo(message: Message):
    if not is_admin(message.from_user.id):
        return
    
    # Bu yerda chekni tekshirish va balans to'ldirish
    await message.answer("📸 Chek qabul qilindi. Foydalanuvchi ID sini va summani yuboring:\n\nFormat: <user_id> <summa>\nMasalan: 123456789 50000")
    await message.reply_to_message.delete()

@router.message(F.text.regexp(r'^\d+\s+\d+$'))
async def admin_process_check(message: Message):
    if not is_admin(message.from_user.id):
        return
    
    try:
        user_id, amount = map(int, message.text.split())
        
        # Balansni to'ldirish
        await db.update_balance(
            user_id=user_id,
            amount=amount,
            transaction_type="payment_approved",
            description=f"To'lov tasdiqlandi. Chek: {message.date}"
        )
        
        new_balance = await db.get_user_balance(user_id)
        
        text = f"""✅ **To'lov tasdiqlandi!**

👤 Foydalanuvchi ID: {user_id}
💰 Summa: {amount:,} so'm
🏦 Yangi balans: {new_balance:,} so'm

💳 Admin: @{message.from_user.username}"""
        
        await message.answer(text)
        
        # Foydalanuvchiga xabar
        from main import bot
        try:
            await bot.send_message(
                chat_id=user_id,
                text=f"✅ To'lovingiz tasdiqlandi! {amount:,} so'm hisobingizga qo'shildi. Yangi balans: {new_balance:,} so'm"
            )
        except:
            pass
            
    except Exception as e:
        await message.answer(f"Xatolik: {e}")
