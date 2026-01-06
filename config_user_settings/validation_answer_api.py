import asyncio

import pydantic
from pydantic_async_validation import async_field_validator, AsyncValidationModelMixin, ValidationInfo


class ValidationDataApi(AsyncValidationModelMixin, pydantic.BaseModel):
    Authorization: str
    Accept: str
    Origin: str
    Referer: str
    User_Agent: str
    
    @async_field_validator('Authorization')
    async def check_authorization(self, auth: str) -> str:
        if isinstance(auth, str) or not auth.strip() != '':
            return auth
        else:
            raise ValueError('Authorization не валиден, type:{}'.format(type(auth)))

    @async_field_validator('Accept')
    async def check_accept(self, accept: str) -> str:
        if isinstance(accept, str or not accept.strip() != ''):
            return accept
        else:
            raise ValueError('Accept не валиден, type: {}'.format(type(accept)))

    @async_field_validator('Origin')
    async def check_accept(self, origin: str) -> str:
        if isinstance(origin, str or not origin.strip() != ''):
            return origin
        else:
            raise ValueError('Origin не валиден, type: {}'.format(type(origin)))

    @async_field_validator('Referer')
    async def check_accept(self, referer: str) -> str:
        if isinstance(referer, str or not referer.strip() != ''):
            return referer
        else:
            raise ValueError('Referer не валиден, type: {}'.format(type(referer)))

    @async_field_validator('User_Agent')
    async def check_accept(self, user_agent: str) -> str:
        if isinstance(user_agent, str or not user_agent.strip() != ''):
            return user_agent
        else:
            raise ValueError('User-Agent не валиден, type: {}'.format(type(user_agent)))

data_for_api = {
    'accept': 'application/json, text/plain, */*',  # ожидаемый результат в формате json
    'accept-language': 'ru_RU, ru','authorization': 'Bearer null','content-type': 'application/json',  # говорим о том что отправляем на сервак# 'origin': 'https://journal.top-academy.ru',  # обязательно для безопастности (Cros защита)
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

async def get_