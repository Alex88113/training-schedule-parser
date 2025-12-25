import asyncio
import pytest
from .config_settings import AuthSettings
from dotenv import load_dotenv
import os

top_username = os.getenv('TOP_USERNAME')
password = os.getenv('PASSWORD')
application_key = os.getenv('APPLICATION_KEY')

class TestingEnv:
    @pytest.mark.asyncio
    async def test_username(self):
        auth_setting = AuthSettings()
        await asyncio.sleep(1)
        assert auth_setting.TOP_USERNAME == top_username
        print('Тест с проверкой логина успешно пройден!')

    @pytest.mark.asyncio
    async def test_password(self):
       auth_setting = AuthSettings()
       assert auth_setting.PASSWORD == password
       print('Тест с паролем успешно пройден!')

    @pytest.mark.asyncio
    async def test_application_key(self):
        auth_setting = AuthSettings()
        assert auth_setting.APPLICATION_KEY == application_key
        print('Тестирование токена авторизации завершено')