from auth import AuthClient
from parser import getting_schedule
import asyncio


async def main():
    obj_class = AuthClient()
    token_schedule = await obj_class. get_authorization()
    result = await getting_schedule(token_schedule)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())