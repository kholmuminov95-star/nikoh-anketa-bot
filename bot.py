import os
TOKEN = os.environ.get("BOT_TOKEN")
ADMIN = os.environ.get("ADMIN_ID")

from aiogram import Bot, Dispatcher, executor, types

TOKEN = "8219884908:AAHMBf0JP1Cd_w2aGlN_cl_CZmyGoV1gAK4"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def start(msg: types.Message):
    await msg.answer("Bot Railway’da ishlayapti ✅")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
