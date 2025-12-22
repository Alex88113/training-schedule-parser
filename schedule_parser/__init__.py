from .auth import AuthClients
from .parser import getting_schedule
import asyncio


async def main():
    obj_class = AuthClients()
    token_schedule:str = await obj_class. get_authorization()
    result = await getting_schedule(token_schedule)
    return result
