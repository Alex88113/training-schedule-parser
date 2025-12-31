from loggers_module.logger_module import *

try:
    from .auth import AuthClients
    from .parser import getting_schedule
    from config_user_settings.config_settings import *
    logger.info('Модули: auth и parser успешно импортированы!')

except (ModuleNotFoundError, ImportError) as error:
    logger.error(f'error import: {e}', e=error)

import asyncio


async def main():
    obj_class = AuthClients(user_data=user_data)
    token_schedule: str = await obj_class.get_authorization()
    result = await getting_schedule(token_schedule)
    return result