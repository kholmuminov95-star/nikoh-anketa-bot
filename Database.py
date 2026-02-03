    async def get_user(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            row = await cursor.fetchone()
            if row:
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, row))
            return None
    
    async def get_user_gender(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT gender FROM users WHERE user_id = ?', (user_id,))
            row = await cursor.fetchone()
            return row[0] if row else None
    
    async def get_user_profile(self, user_id):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT * FROM profiles WHERE user_id = ? ORDER BY created_at DESC LIMIT 1', (user_id,))
            row = await cursor.fetchone()
            if row:
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, row))
            return None
