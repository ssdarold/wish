import sqlite3

def GetUserID(telegram_id):
    try:
        # Подключение к базе данных
        conn = sqlite3.connect('./db.sqlite3')
        cursor = conn.cursor()

        # Получение значения столбца id из таблицы main_user по tg_id
        cursor.execute("SELECT id FROM main_user WHERE tg_id = ?", (telegram_id,))
        result = cursor.fetchone()

        # Закрытие соединения
        conn.close()

        # Если результат не None, возвращаем первый столбец приведенный к типу integer
        return int(result[0]) if result else None

    except Exception as e:
        # Обработка исключения и возврат None в случае ошибки
        print(f"Error getting user ID: {e}")
        return None

