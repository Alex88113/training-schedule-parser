import asyncio
from logger_module import logger
import functools
from typing import Callable, Any

def create_loggers_decorator(function: Callable):
    @functools.wraps(function) # сохраняю метаданные функции
    async def wrapper(self, *args: Any, **kwargs: Any):
        logger.info('производится запуск функции {f}() ', f=function.__name__)
        result = await function(self, *args, **kwargs)
        logger.info('Работа метода: {r} завершена!', r=function.__name__)
        logger.info('Результат: {r}', f=function.__name__, r=result)
        logger.info('-' * 80, '\n')
        return result
    return wrapper
