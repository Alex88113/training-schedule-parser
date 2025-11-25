import asyncio
import aiohttp
import json

API_URL = "https://msapi.top-academy.ru/api/v2/auth/login"
login = 'Kuche_mu73'
password = '6C3f6G3p'

async def post_data(api_url, data):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://journal.top-academy.ru',
        'Referer': 'https://journal.top-academy.ru/'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, json=data, headers=headers) as response:
            print(f'Статус: {response.status}')
            print(f'Headers: {dict(response.headers)}')

            if response.status == 200:
                response_data = await response.json()
                print(f'Успешный ответ: ')
                print(json.dumps(response_data, indent=2, ensure_ascii=False))
                return response_data
            else:
                print(f'Ошибка: {response.status}')
                error_text = await response.text()
                print(f'Текст ошибки: {error_text}')
                return None

async def my_login():
    url = "https://msapi.top-academy.ru/api/v2/auth/login"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://journal.top-academy.ru',
        'Referer': 'https://journal.top-academy.ru/'
    }
    user_data = {
        'application_key': "6a56a5df2667e65aab73ce76d1dd737f7d1faef9c52e8b8c55ac75f565d8e8a6",
        "password": password,
        "username": login
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=user_data, headers=headers) as response:
            print(f"Текущий статус: {response.status}")
            if response.status == 200:
                data_response = await response.json()
                print('Успешный ответ: Токен получен!')
                return data_response['access_token']
            else:
                return 'ошибка входа'

async def homework(access_token):
    url = "https://msapi.top-academy.ru/api/v2/count/homework"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Application-key': "6a56a5df2667e65aab73ce76d1dd737f7d1faef9c52e8b8c55ac75f565d8e8a6",
        'Referer': 'https://journal.top-academy.ru/'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            print(f'Текущий статус домашки: {response.status}')
            if response.status == 200:
                data_homework = await response.json()
                print('Ура страница с домашкой доступна!')
                print(json.dumps(data_homework, indent=2))
                return data_homework

            else:
                print(response.status)
                error_text = response.text()
                print(f'Ошибка из за: {error_text}')
                return None


async def get_schedule(access_token, date="2025-11-26"):
    url_schedule = f"https://msapi.top-academy.ru/api/v2/schedule/operations/get-month?date_filter={date}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'Application-key': "6a56a5df2667e65aab73ce76d1dd737f7d1faef9c52e8b8c55ac75f565d8e8a6",
        'Referer': 'https://journal.top-academy.ru/'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url_schedule, headers=headers) as response:
            print(f'Статус: {response.status}')
            if response.status == 200:
                print('Ура доступ к учебному расписанию есть!')
                data_schedule = await response.json()

                print('=============Моё расписание==============\n')
                for lesson in data_schedule:
                    subject = lesson['subject_name']
                    teacher =lesson['teacher_name']
                    room = lesson['room_name']
                    try:
                        subject = subject.encode('latin-1').decode('unicode_escape')
                        teacher = teacher.encode('latin-1').decode('unicode_escape')
                        room = room.encode('latin-1').decode('unicode_escape')
                    except Exception as error:
                        print(f'Ошибка с кодировкой: {error}')

                    print(f'\n{lesson['date']} | {lesson['lesson']} пара')
                    print(f'начало пары {lesson['started_at']} - {lesson['finished_at']}')
                    print(f'Предмет: {subject}')
                    print(f'Преподаватель: {teacher}')
                    print(f'Аудитория: {room}')
                    print('====================================================================')
                return data_schedule

            else:
                error_text = response.text()
                print(f'Ошибка: {response.status}')
                print(f'Именно: {error_text}')

async def main():
    print('Запуск рабочего прототипа!\n')
    token = await my_login()
    result = await get_schedule(token)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
ъ
