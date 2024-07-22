import asyncio

import logging
from config import TOKEN
from aiogram import Bot, Dispatcher
from app.handlers import router
from app.exchange_service import update_exchange_rates

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def on_startup(dispatcher):
    await update_exchange_rates()

async def main():
    dp.include_router(router)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())    
    except KeyboardInterrupt:
        print("Exit")    