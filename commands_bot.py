import os
import asyncio
from schedule_parser.auth import AuthClients
from schedule_parser.parser import getting_schedule
from loguru import logger
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import sys
from dotenv import load_dotenv

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
    obj_class = AuthClients()
    token = await obj_class.get_authorization()
    schedule = await getting_schedule(token)
    return schedule

@dp.message(Command('schedule'))
async def getting_my_schedule(message: types.Message):
    result = await get_schedule()
    await message.answer(result)