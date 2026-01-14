import asyncio
from typing import Dict, Any

import logging

import aiohttp
from aiohttp import BasicAuth
from pydantic import BaseModel, ValidationError

from abc import ABC, abstractmethod

logging.basicConfig(level=logging.DEBUG)

class SettingsConnector(BaseModel):
    limit: int | None
    limit_per_host: int | None
    ttl_dns_cache: int | None

    def create_settings_connector(self) -> aiohttp.TCPConnector:
        params = {}

        if self.limit is not None:
            params['limit'] = self.limit
        if self.limit_per_host is not None:
            params['limit_per_host'] = self.limit_per_host
        if self.ttl_dns_cache is not None:
            params['ttl_dns_cache'] = self.ttl_dns_cache

        return aiohttp.TCPConnector(**params)

def create_settings():
    try:
        settings = {
            'limit': 100,
            'limit_per_host': 30,
            'ttl_dns_cache': 500
        }
        obj = SettingsConnector(**settings)
        return obj.create_settings_connector()

    except ValidationError as error_valid:
        raise ValueError(
            f'Возникла ошибка при валидации сетевых настроек соединения'
            f'error: {error_valid}')


class TimeoutClient(BaseModel):
    total: int | None
    connect: int | None
    sock_read: int | None
    sock_connect: int | None

    def create_timeout_client(self) -> aiohttp.ClientTimeout:
        params = {}

        if self.total is not str:
            params['total'] = self.total
        if self.connect is not str:
            params['connect'] = self.connect
        if self.sock_read is not str:
            params['sock_read'] = self.sock_read
        if self.sock_connect is not str:
            params['sock_read'] = self.sock_connect

        return aiohttp.ClientTimeout(**params)


def result_time_client():
    try:
        timeout = {
            'total': 30,
            'connect': 15,
            'sock_connect': None,
            'sock_read': None
        }
        result = TimeoutClient(**timeout)
        return result.create_timeout_client()

    except ValidationError as error_valid:
        raise ValueError(f'Возникла ошибка при валидации данных таймаутов'
                         f'error: {error_valid}')


class AuthorizationClient(ABC):
    def __init__(self, application_key: str):
        self.base_url = 'https://msapi.top-academy.ru/api/v2'
        self.session: None = None
        self.auth_token = None
        self.application_key = application_key
        self.conn = create_settings()
        self.timeout = result_time_client()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(connector=self.conn, timeout=self.timeout)
        return self

    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()

    @abstractmethod
    async def login(self, username: str, password: str):
        pass

    @abstractmethod
    async def get_protected_data(self, endpoint: str):
        pass

class AuthClient(AuthorizationClient):
    async def login(self, username: str, password: str) -> bool:
        login_url = f'{self.base_url}/auth/login'

        login_data = {
            'username': username,
            'password': password,
            'application_key': self.application_key
        }

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 YaBrowser/25.12.0.0 Safari/537.36',
            'Origin': 'https://journal.top-academy.ru',
            'Referer': 'https://journal.top-academy.ru/'
        }

        try:
            async with self.session.post(login_url, json=login_data, headers=headers) as resp:
                logging.info(resp.status)
                if resp.status == 200:
                    data = await resp.json()
                    self.auth_token = data.get('refresh_token')
                    logging.info('Авторизация прошла успешно')
                    return True
                else:
                    error_text = await resp.text()
                    logging.warning(f'Причина {error_text}')
                return False
        except aiohttp.ClientConnectorError as error:
            logging.error(f'Не удалось подключится к серверу: {error}')

        except Exception as error:
            print(f'произошла непредвиденная ошибка: {error}')

    async def get_protected_data(self, endpoint: str):
        if not self.auth_token:
            logging.warning('Сначала выполните авторизацию')

        url = f"{self.base_url}{endpoint}"
        headers = {
            'Authorization': f'Bearer {self.auth_token}',
            'Application-Key': self.application_key
        }
        logging.warning(f'Запрашиваю данные с {url}')

        try:
            async with self.session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    logging.info(f'Полученные данные: {data} от endpoint: {endpoint}')
                    return data
                else:
                    error_text = await resp.text()
                    logging.info(f'Запрос к {endpoint} отклонен. статус: {resp.status}'
                          f'Причина {error_text}')
                    return None

        except Exception as error:
            logging.error(f'произошла непредвиденная ошибка: {error}')

