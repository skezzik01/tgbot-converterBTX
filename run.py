import sys
import logging
import asyncio
from threading import Thread
import schedule

from aiogram import Bot, Dispatcher

from app.handlers import router
from app.admins import router as admin_router
import app.convert as convert
from app.database.models import async_main
from config import TOKEN


async def main():
    await async_main()
    
    bot = Bot(token=TOKEN, parse_mode='HTML')
    dp = Dispatcher()
    dp.include_routers(router, admin_router, convert.router) # Роутеры
    
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped')