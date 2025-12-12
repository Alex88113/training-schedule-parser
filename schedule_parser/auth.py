from typing import Dict
import asyncio
import os
from aiohttp import (
    ClientConnectionError,
    ServerConnectionError
)
import aiohttp
from loggers_module.logger_module import logger
from config_settings import AuthSettings
from datetime import datetime

class AuthClient:
    def __init__(self, settings: AuthSettings | None = None):
        self.settings = settings or AuthSettings()

        self.username = self.settings.TOP_USERNAME
        self.password = self.settings.PASSWORD
        self.application_key = self.settings.APPLICATION_KEY
        self.id_city = self.settings.ID_CITY
        self.base_url = 'https://msapi.top-academy.ru/api/v2/auth/login'


        if self.settings.ID_CITY and self.settings.ID_CITY.lower() != 'none':
            try:
                self.id_city = int(self.settings.ID_CITY)
            except ValueError as error:
                logger.error("ошибка: {e} | вторая причина: {e2}", e=error, e2=self.settings.ID_CITY)
        logger.debug('Переменные окружения загружены!')


    async def get_authorization(self):
        headers = {
            'accept': 'application/json, text/plain, */*',  # ожиадаемый результат в формате json
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
            'username': self.username,
            'password': self.password,
            'application_key': self.application_key,
            'id_city': self.id_city
        }
        logger.debug('Производится отправка данных на сервер...')
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(60)) as session:
                async with session.post(self.base_url, headers=headers, json=user_data) as response:
                    logger.debug('Status: {r}', r=response.status)
                    if response.status == 200:
                       logger.debug('Авторизация прошла успешно!')
                       token = await response.json()
                       logger.success('Токен получен: {r}', r=token['access_token'][:30])
                       return token
                    else:
                       error_data = await response.text()
                       logger.error('Произошла ошибка при авторизации: {e}', e=error_data)
        except ServerConnectionError as error:
            logger.error('Ошибка со стороны сервера: {e}', e=error)
        except ClientConnectionError as error_connect:
            logger.error('Возникла ошибка при подключении к серверу: {e}', e=error_connect)
        except ConnectionRefusedError as error:
            logger.error('соединение было отклонено.\nПричина: {e}', e=error)

    async def get_training_schedule(self, token: str):
        today_date = datetime.now().strftime("%Y-%m-%d")
        headers = {
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvbXNhcGkuaXRzdGVwLm9yZyIsImlhdCI6MTc2NTUzMzIwMiwiYXVkIjoxLCJleHAiOjE3NjU1NTQ4MDIsImFwaUFwcGxpY2F0aW9uSWQiOjEsImFwaVVzZXJUeXBlSWQiOjEsInVzZXJJZCI6NjEsImlkQ2l0eSI6NTkyfQ.Ghu_QOKnETNLkTimMlO1SGA-7oExAk4VoS6u2oVfO7k",
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
        params = {
            'date': today_date
        }

        url_schedule: str = f"https://msapi.top-academy.ru/api/v2/schedule/operations/get-by-date?date_filter={today_date}"

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=60)) as session:
            async with session.get(url_schedule, headers=headers, params=params) as response:
                if response.status == 200:
                    response_data = await response.json()
                    print(type(response_data))
                    logger.info('===================================================== Учебное расписание =====================================================\n')
                    for value in response_data[0:]:
                        logger.success('Расписание Успешно получено!')
                        logger.info('Дата занятия: {date}', date=value['date'])
                        logger.info('Пара: {couple}  | преподаватель: {teacher} | Тип пары: {type_couple}',
                                    couple=value['subject_name'], teacher=value['teacher_name'],
                                    type_couple=value['room_name'])
                        logger.info('Начало {start} | Конец {end}', start=value['started_at'], end=value['finished_at'])
                        logger.info('-' * 125)
                        logger.info('\n')
                    logger.info('==============================================================================================================================')
                else:
                    error_text = await response.text()
                    print('Ошибка неверные данные авторизации')
                    print('data error: {}'.format(error_text))


async def main():
    obj = AuthClient()
    token= await obj.get_authorization()
    result = await obj.get_training_schedule(token)
    print(result)

asyncio.run(main())

