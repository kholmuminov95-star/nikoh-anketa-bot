from config import USD_TO_UZS, BONUS_300K, BONUS_500K, BONUS_1M

def calculate_bonus(amount_uzs: int) -> int:
    """Bonusni hisoblash"""
    if amount_uzs >= 1000000:
        return int(amount_uzs * BONUS_1M)
    elif amount_uzs >= 500000:
        return int(amount_uzs * BONUS_500K)
    elif amount_uzs >= 300000:
        return int(amount_uzs * BONUS_300K)
    return 0

def validate_age(text: str):
    """Yoshni tekshirish (18-99)"""
    try:
        age = int(text)
        if 18 <= age <= 99:
            return age
        return None
    except:
        return None

def validate_height(text: str):
    """Bo'yni tekshirish (100-250)"""
    try:
        height = int(text)
        if 100 <= height <= 250:
            return height
        return None
    except:
        return None

def validate_weight(text: str):
    """Vaznni tekshirish (30-200)"""
    try:
        weight = int(text)
        if 30 <= weight <= 200:
            return weight
        return None
    except:
        return None

def validate_languages(text: str):
    """Tillar sonini tekshirish (1-10)"""
    try:
        languages = int(text)
        if 1 <= languages <= 10:
            return languages
        return None
    except:
        return None

def format_profile(profile_data: dict, gender: str) -> str:
    """Profil ma'lumotlarini formatlash"""
    text = f"📋 **PROFIL MA'LUMOTLARI**\n\n"
    
    # Umumiy ma'lumotlar
    text += f"🎂 **Yosh:** {profile_data.get('age')} yosh\n"
    text += f"📏 **Bo'y:** {profile_data.get('height')} sm\n"
    text += f"⚖️ **Vazn:** {profile_data.get('weight')} kg\n"
    text += f"🌍 **Millat:** {profile_data.get('nationality')}\n"
    text += f"💍 **Oilaviy holat:** {profile_data.get('marital_status')}\n"
    
    # Farzandlar (agar kerak bo'lsa)
    if profile_data.get('marital_status') in ['Ajrashgan', 'Beva']:
        children = profile_data.get('children', 0)
        text += f"👶 **Farzandlar:** {children if children > 0 else 'Yo\\'q'}\n"
    
    # Ayollar uchun qo'shimcha
    if gender.lower() == 'ayol':
        hijab = 'Ha' if profile_data.get('hijab') else "Yo'q"
        text += f"🧕 **Ro\\'mol:** {hijab}\n"
        
        move = 'Ha' if profile_data.get('ready_to_move') else "Yo'q"
        text += f"✈️ **Ko\\'chishga tayyor:** {move}\n"
        
        text += f"👰 **2-likka rozilik:** {profile_data.get('ready_for_second_wife')}\n"
    
    # Manzil
    country = profile_data.get('country', '')
    region = profile_data.get('region', '')
    if region:
        text += f"📍 **Manzil:** {country}, {region}\n"
    else:
        text += f"📍 **Manzil:** {country}\n"
    
    # Asli qayerlik
    origin_country = profile_data.get('origin_country', '')
    origin_region = profile_data.get('origin_region', '')
    if origin_region:
        text += f"🎯 **Asli qayerlik:** {origin_country}, {origin_region}\n"
    elif origin_country:
        text += f"🎯 **Asli qayerlik:** {origin_country}\n"
    
    # Din va til
    prays = 'Ha' if profile_data.get('prays') else "Yo'q"
    text += f"📿 **Namoz va Qur\\'on:** {prays}\n"
    text += f"🗣️ **Tillarni bilish:** {profile_data.get('languages')} ta\n"
    
    # Matnli qismlar
    about = profile_data.get('about', '')
    if about:
        text += f"📝 **O\\'zi haqida:** {about[:100]}...\n"
    
    requirements = profile_data.get('requirements', '')
    if requirements:
        if gender.lower() == 'erkak':
            text += f"💭 **Kelin uchun talablar:** {requirements[:100]}...\n"
        else:
            text += f"💭 **Kuyov uchun talablar:** {requirements[:100]}...\n"
    
    # Kim to'ldirdi
    filled_by = profile_data.get('filled_by', '')
    text += f"👤 **To\\'ldirgan:** {filled_by}\n"
    
    # Bog'lanish
    text += f"\n📞 **Bog\\'lanish:** @Hayrli_nikoh_admin"
    
    return text