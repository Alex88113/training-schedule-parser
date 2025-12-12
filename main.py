import os
import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv
import sys

logger.remove()
logger.add(sys.stderr, format='{time} {level} {message}', level='INFO')
load_dotenv()

bot = Bot(token=os.getenv('TOKEN_MY_BOT'))
dp = Dispatcher()
logger.info('Бот создан!')

@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('Hello Alex!')


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logger.info('БОТ ЗАПУЩЕН!')
    asyncio.run(main())