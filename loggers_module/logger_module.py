from loguru import logger
import sys


logger.add(sys.stdout, colorize=True, format='<green>{time}</green> <level>{message}</level>', level='INFO')
logger.add(sys.stdout, colorize=True, format='<yellow>{time}</yellow> <level>{message}</level>', level='SUCCESS')

def create_logger_for_debug():
    logger.add(
    'logs/debug.log',
    format='{time:YYY-MM-DD at HH:mm:ss} | {level} | {message}',
    filter=lambda record: record['level'].name == 'DEBUG',
    level='DEBUG',
    rotation='100 MB'
    )

def create_logger_for_warning():
    logger.add(
    'logs/warning.log',
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    filter=lambda record: record['level'].name == 'WARNING',
    level='WARNING',
    rotation='100 MB'
    )

def create_logger_for_error():
    logger.add(
    'logs/error.log',
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    filter=lambda record: record['level'].name == 'ERROR', # в начале сравнивал объект со строкой
    level='ERROR',
    rotation='500 MB'
    )

def create_logger_for_critical():
    logger.add(
    'logs/critical_error.log',
    format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}',
    filter=lambda record: record['level'].name == 'CRITICAL',
    level='CRITICAL',
    rotation='300 MB'
    )

def main():
    create_logger_for_debug()
    create_logger_for_warning()
    create_logger_for_error()
    create_logger_for_critical()

if __name__ == '__main__':
    main()

