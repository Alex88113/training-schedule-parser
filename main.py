from commands_bot import *
from loggers_module.logger_module import logger

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logger.info('Бот успешно запущен!')
    asyncio.run(main())
