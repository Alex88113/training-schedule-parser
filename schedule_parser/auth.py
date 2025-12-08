import asyncio
import os
from aiohttp import (
    ClientConnectionError,
    ServerConnectionError
)
import aiohttp
from loggers_module.logger_module import logger
from config_settings import AuthSettings

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


    @create_loggers_decorator
    async def get_authorization(self):
        headers = {
            'accept': 'application/json, text/plain, */*',  # ожиадаемый результат в формате json
            'accept-language': 'ru_RU, ru',
            'authorization': 'Bearer null',
            'content-type': 'application/json',  # говорим о том что отправляем на сервак
            'origin': 'https://journal.top-academy.ru',  # обязательно для безопастности (Cros защита)
            'referer': 'https://journal.top-academy.ru/',  # желательно
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
            async with aiohttp.ClientSession() as session:
                async with session.post(self.base_url, headers=headers, json=user_data) as response:
                    logger.debug('Status: {r}', r=response.status)
                    if response.status == 200:
                       logger.debug('Авторизация прошла успешно!')
                       response_data = await response.json()
                       logger.success('Токен получен: {r}', r=response_data['access_token'][:30])
                       return 'Получен токен: {}'.format(response_data['access_token'][:30])
                    else:
                       error_data = await response.text()
                       logger.error('Произошла ошибка при авторизации: {e}', e=error_data)
        except ServerConnectionError as error:
            logger.error('Ошибка со стороны сервера: {e}', e=error)
        except ClientConnectionError as error_connect:
            logger.error('Возникла ошибка при подключении к серверу: {e}', e=error_connect)
        except ConnectionRefusedError as error:
            logger.error('соединение было отклонено.\nПричина: {e}', e=error)



async def main():
    obj = AuthClient()
    print('-' * 80)
    await obj.get_authorization()

asyncio.run(main())