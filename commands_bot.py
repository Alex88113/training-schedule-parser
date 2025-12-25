import sys
import os
import asyncio

from loguru import logger
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config_user_settings.config_settings import *
from aiogram import F
from dotenv import load_dotenv

from schedule_parser.auth import AuthClients
from schedule_parser.parser import getting_schedule

load_dotenv()


def setup_package_path():
    """Добавляет корневую директорию проекта в sys.path"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)  # Поднимаемся на уровень выше

    if project_root not in sys.path:
        sys.path.insert(0, project_root)
        logger.info(f"Added to sys.path: {project_root}")


setup_package_path()

try:
    from schedule_parser.auth import AuthClients
    from schedule_parser.parser import getting_schedule

    logger.info("Модули schedule_parser успешно импортированы")
except ImportError as e:
    logger.error(f"Ошибка импорта: {e}")
    raise

logger.remove()
logger.add(sys.stderr, format='{time} | {level} | {message}', level='INFO')

bot = Bot(os.getenv('TOKEN_MY_BOT'))
dp = Dispatcher()
logger.info('БОТ СОЗДАН!')

async def get_schedule():
    obj_class = AuthClients(user_data=user_data)
    token = await obj_class.get_authorization()
    schedule = await getting_schedule(token)
    return schedule

@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text='Учебное расписание на сегодня')]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    await message.answer('Хотите ли вы увидеть учебное расписание на сегодня?', reply_markup=keyboard)

@dp.message(F.text.lower().capitalize().strip() == 'Учебное расписание на сегодня')
async def input_schedule(message: types.Message):
    result = await get_schedule()
    await message.answer(result)

