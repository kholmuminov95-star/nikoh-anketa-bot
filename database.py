import asyncpg
import logging
from config import DATABASE_URL

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.db_url = DATABASE_URL
    
    async def init_db(self):
        """Database va jadvallarni yaratish"""
        conn = await asyncpg.connect(self.db_url)
        
        # Users jadvali
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id BIGINT PRIMARY KEY,
                phone VARCHAR(20),
                first_name VARCHAR(100),
                username VARCHAR(100),
                gender VARCHAR(10),
                age INTEGER,
                height INTEGER,
                weight INTEGER,
                nationality VARCHAR(50),
                marital_status VARCHAR(50),
                children INTEGER DEFAULT 0,
                country VARCHAR(100),
                region VARCHAR(100),
                origin_country VARCHAR(100),
                origin_region VARCHAR(100),
                prays BOOLEAN,
                languages INTEGER,
                about TEXT,
                requirements TEXT,
                hijab BOOLEAN,
                ready_to_move BOOLEAN,
                ready_for_second_wife VARCHAR(50),
                filled_by VARCHAR(50),
                balance BIGINT DEFAULT 0,
                bonus_received BOOLEAN DEFAULT FALSE,
                profile_completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Profillar jadvali
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS profiles (
                profile_id SERIAL PRIMARY KEY,
                user_id BIGINT REFERENCES users(user_id),
                gender VARCHAR(10),
                age INTEGER,
                height INTEGER,
                weight INTEGER,
                nationality VARCHAR(50),
                marital_status VARCHAR(50),
                children INTEGER DEFAULT 0,
                country VARCHAR(100),
                region VARCHAR(100),
                origin_country VARCHAR(100),
                origin_region VARCHAR(100),
                prays BOOLEAN,
                languages INTEGER,
                about TEXT,
                requirements TEXT,
                hijab BOOLEAN,
                ready_to_move BOOLEAN,
                ready_for_second_wife VARCHAR(50),
                filled_by VARCHAR(50),
                is_public BOOLEAN DEFAULT FALSE,
                is_vip_only BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        await conn.close()
        logger.info("✅ Database jadvallari yaratildi")
    
    async def add_user(self, user_id, phone, first_name, username):
        """Yangi foydalanuvchi qo'shish"""
        conn = await asyncpg.connect(self.db_url)
        await conn.execute('''
            INSERT INTO users (user_id, phone, first_name, username)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (user_id) DO UPDATE 
            SET phone = $2, first_name = $3, username = $4
        ''', user_id, phone, first_name, username)
        await conn.close()
    
    async def get_user(self, user_id):
        """Foydalanuvchini olish"""
        conn = await asyncpg.connect(self.db_url)
        row = await conn.fetchrow('SELECT * FROM users WHERE user_id = $1', user_id)
        await conn.close()
        return dict(row) if row else None
    
    async def update_user_profile(self, user_id, **kwargs):
        """Foydalanuvchi profilini yangilash"""
        if not kwargs:
            return
        
        conn = await asyncpg.connect(self.db_url)
        
        # Dinamik UPDATE query yaratish
        set_parts = []
        values = []
        i = 1
        
        for key, value in kwargs.items():
            set_parts.append(f"{key} = ${i}")
            values.append(value)
            i += 1
        
        set_clause = ", ".join(set_parts)
        values.append(user_id)
        
        query = f'''
            UPDATE users 
            SET {set_clause}, profile_completed = TRUE 
            WHERE user_id = ${i}
        '''
        
        await conn.execute(query, *values)
        await conn.close()