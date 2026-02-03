from config import USD_TO_UZS, BONUS_300K, BONUS_500K, BONUS_1M

def calculate_bonus(amount_uzs):
    """Bonusni hisoblash"""
    if amount_uzs >= 1000000:
        return int(amount_uzs * BONUS_1M)
    elif amount_uzs >= 500000:
        return int(amount_uzs * BONUS_500K)
    elif amount_uzs >= 300000:
        return int(amount_uzs * BONUS_300K)
    return 0

def format_balance(balance_uzs):
    """Balansni formatlash"""
    usd = balance_uzs / USD_TO_UZS
    return f"Balans: {balance_uzs:,} so'm (${usd:.2f})"

def validate_age(age_text):
    """Yoshni tekshirish"""
    try:
        age = int(age_text)
        if 18 <= age <= 99:
            return age
        return None
    except:
        return None

def validate_height(height_text):
    """Bo'yni tekshirish"""
    try:
        height = int(height_text)
        if 100 <= height <= 250:
            return height
        return None
    except:
        return None

def validate_weight(weight_text):
    """Vaznni tekshirish"""
    try:
        weight = int(weight_text)
        if 30 <= weight <= 200:
            return weight
        return None
    except:
        return None

def validate_languages(lang_text):
    """Tillar sonini tekshirish"""
    try:
        lang = int(lang_text)
        if 1 <= lang <= 10:
            return lang
        return None
    except:
        return None

def format_profile(profile_data, gender):
    """Anketani formatlash"""
    text = f"Anketa raqami: #{profile_data.get('profile_id', 'None')}\n\n"
    
    if gender == "male":
        text += f"?? Yosh: {profile_data.get('age')}\n"
        text += f"?? Bo'y: {profile_data.get('height')} sm\n"
        text += f"?? Vazn: {profile_data.get('weight')} kg\n"
        text += f"?? Millati: {profile_data.get('nationality')}\n"
        text += f"?? Oilaviy holat: {profile_data.get('marital_status')}\n"
        
        if profile_data.get('marital_status') in ['Ajrashgan', 'Beva']:
            children_text = "Yo'q" if profile_data.get('children', 0) == 0 else profile_data.get('children')
            text += f"?? Farzandi: {children_text}\n"
        
        text += f"?? Manzil: {profile_data.get('country')}"
        if profile_data.get('region'):
            text += f", {profile_data.get('region')}"
        text += "\n"
        
        if profile_data.get('country') != "O'zbekiston":
            text += f"?? Asli qayerlik: {profile_data.get('origin_country')}"
            if profile_data.get('origin_region'):
                text += f", {profile_data.get('origin_region')}"
            text += "\n"
        
        text += f"?? Namoz va Qur'on o'qiysizmi: {'Ha' if profile_data.get('prays') else 'Yo'q'}\n"
        text += f"?? Nechta til bilasiz: {profile_data.get('languages')}\n"
        text += f"?? O'zingiz haqingizda: {profile_data.get('about', '')}\n"
        text += f"?? Kelin uchun talablar: {profile_data.get('requirements', '')}\n"
        text += f"?? Bog'lanish: {profile_data.get('filled_by')}: @Hayrli_nikoh_admin"
    
    else:  # ayol
        text += f"?? Yosh: {profile_data.get('age')}\n"
        text += f"?? Bo'y: {profile_data.get('height')} sm\n"
        text += f"?? Vazn: {profile_data.get('weight')} kg\n"
        text += f"?? Millati: {profile_data.get('nationality')}\n"
        text += f"?? Oilaviy holat: {profile_data.get('marital_status')}\n"
        
        if profile_data.get('marital_status') in ['Ajrashgan', 'Beva']:
            children_text = "Yo'q" if profile_data.get('children', 0) == 0 else profile_data.get('children')
            text += f"?? Farzandi: {children_text}\n"
        
        text += f"?? Ro'mol o'raysizmi: {'Ha' if profile_data.get('hijab') else 'Yo'q'}\n"
        text += f"?? Ko'chib o'tishga tayyormisiz: {'Ha' if profile_data.get('ready_to_move') else 'Yo'q'}\n"
        text += f"?? 2-likka rozimisiz: {profile_data.get('ready_for_second_wife')}\n"
        text += f"?? Manzil: {profile_data.get('country')}"
        if profile_data.get('region'):
            text += f", {profile_data.get('region')}"
        text += "\n"
        
        if profile_data.get('country') != "O'zbekiston":
            text += f"?? Asli qayerlik: {profile_data.get('origin_country')}"
            if profile_data.get('origin_region'):
                text += f", {profile_data.get('origin_region')}"
            text += "\n"
        
        text += f"?? Namoz va Qur'on o'qiysizmi: {'Ha' if profile_data.get('prays') else 'Yo'q'}\n"
        text += f"?? Nechta til bilasiz: {profile_data.get('languages')}\n"
        text += f"?? O'zingiz haqingizda: {profile_data.get('about', '')}\n"
        text += f"?? Kuyov uchun talablar: {profile_data.get('requirements', '')}\n"
        text += f"?? Bog'lanish: {profile_data.get('filled_by')}: @Hayrli_nikoh_admin"
    
    return text
