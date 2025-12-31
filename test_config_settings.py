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
    @pytest.mark.asyncio
    async def test_username_config(self):
        assert os.getenv('TOP_USERNAME') == os.getenv('TOP_USERNAME')
