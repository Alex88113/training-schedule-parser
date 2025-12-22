import asyncio
import os

from aiohttp import (
    ClientConnectionError,
    ServerConnectionError
)
from loguru import logger
import aiohttp

from .config_settings import *
from datetime import datetime
from pydantic import BaseModel


class AuthClients:
    def __init__(self, user_data: dict):
        self.user_data = UserSettings(**user_data)
        self.base_url: str = 'https://msapi.top-academy.ru/api/v2/auth/login'

    async def get_authorization(self):
        headers = {
            'accept': 'application/json, text/plain, */*',  # ожидаемый результат в формате json
            'accept-language': 'ru_RU, ru',
            'authorization': 'Bearer null',
            'content-type': 'application/json',  # говорим о том что отправляем на сервак
            'origin': 'https://journal.top-academy.ru',  # обязательно для безопастности (Cros защита)
            'referer': 'https://journal.top-academy.ru/',  # желательно
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ru_RU, ru",
            'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "YaBrowser";v="25.10", "Yowser";v="2.5"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 YaBrowser/25.10.0.0 Safari/537.36'
        }

        user_data = {
            'username': self.user_data.username,
            'password': self.user_data.password,
            'application_key': self.user_data.application_key,
            'id_city': None
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.base_url, headers=headers, json=user_data) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        return response_data['refresh_token']

        except ServerConnectionError as error_connect:
            logger.error('Ошибка со стороны сервера: {e}', e=error_connect)

        except ClientConnectionError as error:
            logger.error('Возникла ошибка при подключении к серверу: {e}', e=error)

        except ConnectionRefusedError as error:
            logger.error('Соединение отклонено: {e}', e=error)
