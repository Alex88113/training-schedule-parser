from auth import AuthClient
import asyncio
import aiohttp

async def getting_token():
    obj = AuthClient()
    token = await obj.get_authorization()
    return token

async def getting_schedule(token: str) -> str:
    url_schedule: str = "https://msapi.top-academy.ru/api/v2/schedule/operations/get-by-date?date_filter=2025-12-15"
    headers: dict[str, str] = {
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvbXNhcGkuaXRzdGVwLm9yZyIsImlhdCI6MTc2NTY1NDkyMCwiYXVkIjoxLCJleHAiOjE3NjU2NzY1MjAsImFwaUFwcGxpY2F0aW9uSWQiOjEsImFwaVVzZXJUeXBlSWQiOjEsInVzZXJJZCI6NjEsImlkQ2l0eSI6NTkyfQ.zsUsLiqtn-gcMM2omKsm5ZyxGTr_L-dNx5cV5zgfthA",
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://journal.top-academy.ru',
        'Referer': 'https://journal.top-academy.ru/',
        "path": "/api/v2/signal/operations/signals-list",
        "accept-encoding": "gzip, deflate, br, zstd",
        "sec-ch-ua": "Chromium;v=140, Not=A?Brand;v=24, YaBrowser;v=25.10, Yowser;v=2.5",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 YaBrowser/25.10.0.0 Safari/537.36'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url_schedule, headers=headers) as response:
            if response.status == 200:
                schedule_data = await response.json()
                schedule_info: str = '========================Учебное Расписание========================\n'
                for value in schedule_data:
                    schedule_info += f"\nЗанятия на {value['date']}\n"
                    schedule_info += f"Начало занятия {value['started_at']} | Конец {value['finished_at']}\n"
                    schedule_info += f"Название пары: {value['subject_name']} | преподаватель: {value['teacher_name']}\n"
                    schedule_info += f"Аудитория: {value['room_name']}"
                    schedule_info += "\n"
                    schedule_info += "-" * 80
                return schedule_info
