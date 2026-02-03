import aiosqlite
import datetime
from config import DATABASE_PATH

class Database:
    def __init__(self):
        self.db_path = DATABASE_PATH
    
    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            # Foydalanuvchilar jadvali
            await db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    phone TEXT,
                    first_name TEXT,
                    username TEXT,
                    gender TEXT,
                    age INTEGER,
                    height INTEGER,
                    weight INTEGER,
                    nationality TEXT,
                    marital_status TEXT,
                    children INTEGER,
                    country TEXT,
                    region TEXT,
                    origin_country TEXT,
                    origin_region TEXT,
                    prays BOOLEAN,
                    languages INTEGER,
                    about TEXT,
                    requirements TEXT,
                    hijab BOOLEAN,
                    ready_to_move BOOLEAN,
                    ready_for_second_wife TEXT,
                    filled_by TEXT,
                    balance INTEGER DEFAULT 0,
                    bonus_received BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    profile_completed BOOLEAN DEFAULT FALSE
                )
            ''')
            
            # Anketalar jadvali
            await db.execute('''
                CREATE TABLE IF NOT EXISTS profiles (
                    profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    gender TEXT,
                    age INTEGER,
                    height INTEGER,
                    weight INTEGER,
                    nationality TEXT,
                    marital_status TEXT,
                    children INTEGER,
                    country TEXT,
                    region TEXT,
                    origin_country TEXT,
                    origin_region TEXT,
                    prays BOOLEAN,
                    languages INTEGER,
                    about TEXT,
                    requirements TEXT,
                    hijab BOOLEAN,
                    ready_to_move BOOLEAN,
                    ready_for_second_wife TEXT,
                    filled_by TEXT,
                    is_public BOOLEAN DEFAULT FALSE,
                    is_vip_only BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # Tranzaksiyalar jadvali
            await db.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    amount INTEGER,
                    transaction_type TEXT,
                    description TEXT,
                    status TEXT DEFAULT 'pending',
                    payment_method TEXT,
                    receipt_photo TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            
            # So'rovlar jadvali
            await db.execute('''
                CREATE TABLE IF NOT EXISTS requests (
                    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    from_user_id INTEGER,
                    to_profile_id INTEGER,
                    status TEXT DEFAULT 'pending',
                    amount_paid INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (from_user_id) REFERENCES users (user_id),
                    FOREIGN KEY (to_profile_id) REFERENCES profiles (profile_id)
                )
            ''')
            
            await db.commit()
    
    # Foydalanuvchilar bilan ishlash
    async def add_user(self, user_id, phone, first_name, username):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT OR IGNORE INTO users (user_id, phone, first_name, username)
                VALUES (?, ?, ?, ?)
            ''', (user_id, phone, first_name, username))
            await db.commit()
    
    async def update_user_profile(self, user_id, **data):
        async with aiosqlite.connect(self.db_path) as db:
            set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
            values = list(data.values())
            values.append(user_id)
            await db.execute(f'''
                UPDATE users SET {set_clause}, profile_completed = ?
                WHERE user_id = ?
            ''', (*values, True, user_id))
            await db.commit()
    
    # Profillar bilan ishlash
    async def create_profile(self, user_id, **data):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('''
                INSERT INTO profiles (user_id, gender, age, height, weight, nationality, 
                marital_status, children, country, region, origin_country, origin_region,
                prays, languages, about, requirements, hijab, ready_to_move, 
                ready_for_second_wife, filled_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, data.get('gender'), data.get('age'), data.get('height'),
                data.get('weight'), data.get('nationality'), data.get('marital_status'),
                data.get('children'), data.get('country'), data.get('region'),
                data.get('origin_country'), data.get('origin_region'), data.get('prays'),
                data.get('languages'), data.get('about'), data.get('requirements'),
                data.get('hijab'), data.get('ready_to_move'), 
                data.get('ready_for_second_wife'), data.get('filled_by')
            ))
            await db.commit()
            return cursor.lastrowid
    
    # Balans bilan ishlash
    async def update_balance(self, user_id, amount, transaction_type="deposit", description=""):
        async with aiosqlite.connect(self.db_path) as db:
            # Balansni yangilash
            await db.execute('''
                UPDATE users SET balance = balance + ? WHERE user_id = ?
            ''', (amount, user_id))
            
            # Tranzaksiyani qo'shish
            await db.execute('''
                INSERT INTO transactions (user_id, amount, transaction_type, description)
                VALUES (?, ?, ?, ?)
            ''', (user_id, amount, transaction_type, description))
            
            await db.commit()
    
    async def get_user_balance(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
            row = await cursor.fetchone()
            return row[0] if row else 0
    
    async def get_transactions(self, user_id, limit=20):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('''
                SELECT * FROM transactions 
                WHERE user_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (user_id, limit))
            return await cursor.fetchall()
