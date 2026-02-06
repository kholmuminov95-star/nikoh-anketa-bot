from aiogram.fsm.state import State, StatesGroup

class ProfileStates(StatesGroup):
    # Asosiy ma'lumotlar
    waiting_for_gender = State()
    waiting_for_age = State()
    waiting_for_height = State()
    waiting_for_weight = State()
    waiting_for_nationality = State()
    waiting_for_nationality_custom = State()
    waiting_for_marital_status = State()
    waiting_for_children = State()
    
    # Ayollar uchun qo'shimcha
    waiting_for_hijab = State()
    waiting_for_ready_to_move = State()
    waiting_for_second_wife = State()
    
    # Manzil
    waiting_for_country = State()
    waiting_for_region = State()
    waiting_for_origin_country = State()
    waiting_for_origin_region = State()
    
    # Din va til
    waiting_for_prays = State()
    waiting_for_languages = State()
    
    # Matnli javoblar
    waiting_for_about = State()
    waiting_for_requirements = State()
    waiting_for_filled_by = State()
    
    # Tasdiqlash
    confirming_profile = State()

class PaymentStates(StatesGroup):
    waiting_for_payment_method = State()
    waiting_for_amount_usd = State()
    waiting_for_amount_uzs = State()
    confirming_payment = State()
    waiting_for_receipt = State()

class RequestStates(StatesGroup):
    waiting_for_profile_id = State()
    confirming_request = State()

class AdStates(StatesGroup):
    waiting_for_ad_type = State()
    confirming_ad = State()