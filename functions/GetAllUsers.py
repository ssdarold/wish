import sqlite3

def GetAllUsers():
    try:
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()

        # Извлекаем все значения столбца tg_id
        cursor.execute("SELECT tg_id FROM main_user")
        results = cursor.fetchall()

        # Формируем список
        user_ids = [result[0] for result in results]

        conn.close()
        return user_ids
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []

