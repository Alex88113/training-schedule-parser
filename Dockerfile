FROM python:3.12

WORKDIR /training-schedule-parser

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . . #корирование всех оставшихся файлов

CMD ["python", "main.py"]