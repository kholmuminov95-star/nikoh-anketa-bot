from config import USD_TO_UZS, BONUS_300K, BONUS_500K, BONUS_1M

def calculate_bonus(amount_uzs):
    if amount_uzs >= 1000000:
        return int(amount_uzs * BONUS_1M)
    elif amount_uzs >= 500000:
        return int(amount_uzs * BONUS_500K)
    elif amount_uzs >= 300000:
        return int(amount_uzs * BONUS_300K)
    return 0

def format_balance(balance_uzs):
    usd = balance_uzs / USD_TO_UZS
    return f"Balans: {balance_uzs:,} so'm (${usd:.2f})"

def validate_age(age_text):
    try:
        age = int(age_text)
        if 18 <= age <= 99:
            return age
        return None
    except:
        return None

def validate_height(height_text):
    try:
        height = int(height_text)
        if 100 <= height <= 250:
            return height
        return None
    except:
        return None

def validate_weight(weight_text):
    try:
        weight = int(weight_text)
        if 30 <= weight <= 200:
            return weight
        return None
    except:
        return None

def validate_languages(lang_text):
    try:
        lang = int(lang_text)
        if 1 <= lang <= 10:
            return lang
        return None
    except:
        return None

def format_profile(profile_data, gender):
    text = f"Anketa raqami: #{profile_data.get('profile_id', 'None')}\n\n"
    
    yes_no = {True: "Ha", False: "Yo'q"}
    
    if gender == "male" or gender == "Erkak":
        text += f"📅 Yosh: {profile_data.get('age')}\n"
        text += f"📏 Bo'y: {profile_data.get('height')} sm\n"
        text += f"⚖️ Vazn: {profile_data.get('weight')} kg\n"
        text += f"🌍 Millati: {profile_data.get('nationality')}\n"
        text += f"💍 Oilaviy holat: {profile_data.get('marital_status')}\n"
        
        if profile_data.get('marital_status') in ['Ajrashgan', 'Beva']:
            children = profile_data.get('children', 0)
            children_text = "Yo'q" if children == 0 else str(children)
            text += f"👶 Farzandi: {children_text}\n"
        
        location = profile_data.get('country')
        if profile_data.get('region'):
            location += f", {profile_data.get('region')}"
        text += f"📍 Manzil: {location}\n"
        
        if profile_data.get('country') != "O'zbekiston":
            origin = profile_data.get('origin_country')
            if profile_data.get('origin_region'):
                origin += f", {profile_data.get('origin_region')}"
            text += f"🎯 Asli qayerlik: {origin}\n"
        
        prays_text = yes_no.get(profile_data.get('prays'), "Yo'q")
        text += f"📿 Namoz va Qur'on o'qiysizmi: {prays_text}\n"
        
        text += f"🗣️ Nechta til bilasiz: {profile_data.get('languages')}\n"
        text += f"📝 O'zingiz haqingizda: {profile_data.get('about', '')}\n"
        text += f"💭 Kelin uchun talablar: {profile_data.get('requirements', '')}\n"
        
        filled_by = profile_data.get('filled_by', '')
        text += f"👤 Bog'lanish: {filled_by}: @Hayrli_nikoh_admin"
    
    else:  # ayol
        text += f"📅 Yosh: {profile_data.get('age')}\n"
        text += f"📏 Bo'y: {profile_data.get('height')} sm\n"
        text += f"⚖️ Vazn: {profile_data.get('weight')} kg\n"
        text += f"🌍 Millati: {profile_data.get('nationality')}\n"
        text += f"💍 Oilaviy holat: {profile_data.get('marital_status')}\n"
        
        if profile_data.get('marital_status') in ['Ajrashgan', 'Beva']:
            children = profile_data.get('children', 0)
            children_text = "Yo'q" if children == 0 else str(children)
            text += f"👶 Farzandi: {children_text}\n"
        
        hijab_text = yes_no.get(profile_data.get('hijab'), "Yo'q")
        text += f"🧕 Ro'mol o'raysizmi: {hijab_text}\n"
        
        move_text = yes_no.get(profile_data.get('ready_to_move'), "Yo'q")
        text += f"✈️ Ko'chib o'tishga tayyormisiz: {move_text}\n"
        
        text += f"👰 2-likka rozimisiz: {profile_data.get('ready_for_second_wife')}\n"
        
        location = profile_data.get('country')
        if profile_data.get('region'):
            location += f", {profile_data.get('region')}"
        text += f"📍 Manzil: {location}\n"
        
        if profile_data.get('country') != "O'zbekiston":
            origin = profile_data.get('origin_country')
            if profile_data.get('origin_region'):
                origin += f", {profile_data.get('origin_region')}"
            text += f"🎯 Asli qayerlik: {origin}\n"
        
        prays_text = yes_no.get(profile_data.get('prays'), "Yo'q")
        text += f"📿 Namoz va Qur'on o'qiysizmi: {prays_text}\n"
        
        text += f"🗣️ Nechta til bilasiz: {profile_data.get('languages')}\n"
        text += f"📝 O'zingiz haqingizda: {profile_data.get('about', '')}\n"
        text += f"💭 Kuyov uchun talablar: {profile_data.get('requirements', '')}\n"
        
        filled_by = profile_data.get('filled_by', '')
        text += f"👤 Bog'lanish: {filled_by}: @Hayrli_nikoh_admin"
    
    return text
