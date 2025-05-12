# Використовуємо базовий образ Python
FROM python:3.11-slim

WORKDIR /app

COPY app/ .
COPY requirements.txt .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Вказуємо команду для запуску додатка
CMD ["python", "main.py"]