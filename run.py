import asyncio
import logging
import os
from aiogram import Bot,Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from config.conf import TOKEN
from app.handlers import router, force_data_check
from app.backend import update_info_on_start

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    update_info_on_start()
    scheduler = AsyncIOScheduler(timezone="Asia/Novosibirsk")
    scheduler.add_job(force_data_check, "cron", hour=23, minute=30, start_date=datetime.now(), kwargs={'bot': bot})
    scheduler.start()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    os.makedirs("storage",exist_ok=True) # создание хранилища под информацию
    logging.basicConfig(format="{asctime} - {message}", 
                        style="{", 
                        datefmt="%Y-%m-%d %H:%M", 
                        level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
