import asyncio
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import bot_config

loop = asyncio.new_event_loop()
bot = Bot(bot_config.BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, loop=loop, storage=storage)

if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp)
    