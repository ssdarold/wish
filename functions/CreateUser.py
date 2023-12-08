import sqlite3
from datetime import datetime

def CreateUser(tg_id, username):
    try:
        # Подключение к базе данных
        conn = sqlite3.connect('./db.sqlite3')
        cursor = conn.cursor()

        # Проверка наличия пользователя с таким tg_id
        cursor.execute("SELECT 1 FROM main_user WHERE tg_id = ?", (tg_id,))
        user_exists = cursor.fetchone()

        if user_exists:
            return False  # Пользователь уже существует, возвращаем False

        # Создание новой записи с указанием join_date
        join_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO main_user (tg_id, username, join_datetime) VALUES (?, ?, ?)",
                       (tg_id, username, join_date))

        # Сохранение изменений и закрытие соединения
        conn.commit()
        conn.close()

        return True  # Успешно создан новый пользователь

    except Exception as e:
        # Обработка исключения и возврат False в случае ошибки
        print(f"Error creating user: {e}")
        return False


