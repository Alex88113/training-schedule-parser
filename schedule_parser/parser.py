from datetime import *
import asyncio

import aiohttp
from loguru import logger

from config_user_settings.config_settings import *
from .auth import AuthClients


async def getting_schedule(token: str):
    today_date = date.today()
    url_schedule: str = f"https://msapi.top-academy.ru/api/v2/schedule/operations/get-by-date?date_filter=2025-12-25"
    headers = {
        "Authorization": f"Bearer {token}",
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://journal.top-academy.ru',
        'Referer': 'https://journal.top-academy.ru/',
        "path": "/api/v2/signal/operations/signals-list",
        "accept-encoding": "gzip, deflate, br, zstd",
        "sec-ch-ua": "Chromium;v=140, Not=A?Brand;v=24, YaBrowser;v=25.10, Yowser;v=2.5",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 YaBrowser/25.10.0.0 Safari/537.36'
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url_schedule, headers=headers) as response:
                if response.status == 200:
                    schedule_info: str = ''
                    schedule_data = await response.json()
                    for value in schedule_data:
                        schedule_info += f"\n📅 Занятия на {value['date']}\n"
                        schedule_info += f"\n🕗 Начало занятия {value['started_at']} |⌛ Конец {value['finished_at']}\n"
                        schedule_info += f"\n🎓 Название пары: {value['subject_name']} |👨‍🏫 преподаватель: {value['teacher_name']}\n"
                        schedule_info += f"\n🚪 Аудитория: {value['room_name']}"
                        schedule_info += "\n"
                        schedule_info += "-" * 68
                    return schedule_info
                else:
                    error_data: str = await response.text()
                    logger.warning("Не удалось получить расписание.\n Причина: {e}", e=error_data)

    except TimeoutError as error:
        logger.warning('Сайт не ответил на протяжении 30 секунд, из за: {e}',e=error)
