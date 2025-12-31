import asyncio
import os

import aiohttp
import pytest_asyncio
import pytest

from dotenv import load_dotenv

from config_user_settings.config_settings import *

load_dotenv()

class TestSettings:
    """
    Класс TestSettings проверяет корректность пользовательских данных из модуля config_settings.py
    """
    user_data = UserSettings(**user_data)

    @pytest_asyncio.fixture
    async def test_config(self):
        return {
            'username': self.user_data.username,
            'password': self.user_data.password,
            'application_key': self.user_data.application_key,
            'id_city': None
        }

    @pytest.mark.asyncio
    async def test_username_config(self, test_config):
        result ={
            'username': test_config['username']
        }
        assert os.getenv('TOP_USERNAME') == os.getenv('TOP_USERNAME')
