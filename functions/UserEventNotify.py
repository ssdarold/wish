import sqlite3
import datetime
from aiogram import types

async def UserEventNotify():
    try:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        # Получаем значение user_event_delta из таблицы main_settings
        cursor.execute("SELECT user_event_delta FROM main_settings LIMIT 1")
        user_event_delta = cursor.fetchone()[0]

        # Вычисляем текущую дату
        current_date = datetime.datetime.now().date()

        # Извлекаем значения из таблицы main_userevents
        cursor.execute("SELECT user_id, event_name FROM main_userevents WHERE DATE(event_date, '-" + str(user_event_delta) + " days') = DATE(?)", (current_date,))
        results = cursor.fetchall()

        # Отправляем уведомления каждому пользователю
        for result in results:
            user_id, event_name = result
            message_text = f"До вашего события <b>{event_name}</b> осталось {user_event_delta} дней! Успейте подготовить свой wish-лист!"
            await bot.send_message(user_id, message_text, parse_mode=types.ParseMode.HTML)

        conn.close()
    except Exception as e:
        print(f"An error occurred: {str(e)}")