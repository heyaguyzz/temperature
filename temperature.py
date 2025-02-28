import requests
import sqlite3
from datetime import datetime

# налаштування для OpenWeatherMap API
api_key = 'ваш_ключ_API'  # замініть на ваш API-ключ.
city = 'Bad Oeynhausen'
units = 'metric'  # використовуємо метричну систему (градуси Цельсія)
lang = 'uk'  # українська мова.

# отримання даних про погоду.
url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}&lang={lang}'
response = requests.get(url)
data = response.json()

if response.status_code == 200:
    # отримання поточної температури.
    temperature = data['main']['temp']
    print(f"Поточна температура в {city}: {temperature}°C")

    # підключення до бази даних (створення, якщо не існує)
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()

    # створення таблиці, якщо не існує.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT NOT NULL,
            temperature REAL NOT NULL
        )
    ''')

    # отримання поточної дати та часу.
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # вставка даних у таблицю.
    cursor.execute('''
        INSERT INTO weather_data (datetime, temperature)
        VALUES (?, ?)
    ''', (current_datetime, temperature))

    # збереження змін та закриття з'єднання.
    conn.commit()
    conn.close()
else:
    print(f"Не вдалося отримати дані про погоду. Код помилки: {response.status_code}")
