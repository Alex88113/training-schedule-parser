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
        assert result['username'] == os.getenv('TOP_USERNAME')

    @pytest.mark.asyncio
    async def test_password(self, test_config):
        user_password = {'password': test_config['password']}
        assert user_password['password'] == os.getenv('PASSWORD')

    @pytest.mark.asyncio
    async def test_application(self, test_config):
        user_password = {'application_key': test_config['application_key']}
        assert user_password['application_key'] == os.getenv('APPLICATION_KEY')

    @pytest.mark.asyncio
    async def test_id_city(self, test_config):
        user_city = {'id_city': test_config['id_city']}
        assert user_city['id_city'] == None # fix
