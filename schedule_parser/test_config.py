import asyncio
import pytest
from .config_settings import AuthSettings

class TestingEnv:
    @pytest.mark.asyncio
    async def test_username(self):
        auth_setting = AuthSettings()
        await asyncio.sleep(1)
        assert auth_setting.TOP_USERNAME == "Kuche_mu73"

        print(f'Login: {auth_setting.TOP_USERNAME}')
        print('Тест с проверкой логина успешно пройден!')

    @pytest.mark.asyncio
    async def test_password(self):
       auth_setting = AuthSettings()
       assert auth_setting.PASSWORD == '6C3f6G3p'
       print(f'Ваш пароль: {auth_setting.PASSWORD}')
       print('Тест с паролем успешно пройден!')

    @pytest.mark.asyncio
    async def test_application_key(self):
        auth_setting = AuthSettings()
        assert auth_setting.APPLICATION_KEY ==  "6a56a5df2667e65aab73ce76d1dd737f7d1faef9c52e8b8c55ac75f565d8e8a6"
        print(f'Токен авторизации: {auth_setting.APPLICATION_KEY[:20]}')
        print('Тестирование токена авторизации завершено')