import sqlite3

def CheckUserRelation(first_user_id, second_user_id):
    try:
        # Подключение к базе данных
        conn = sqlite3.connect('../db.sqlite3')
        cursor = conn.cursor()

        # Поиск в таблице main_relateduser
        cursor.execute("SELECT * FROM main_relateduser WHERE (first_user_id = ? AND second_user_id = ?) OR (first_user_id = ? AND second_user_id = ?)",
                       (first_user_id, second_user_id, second_user_id, first_user_id))

        # Получение результатов запроса
        result = cursor.fetchall()

        # Проверка наличия хотя бы одного пересечения
        if result:
            return True
        else:
            return False
    except sqlite3.Error as e:
        print("Error checking user relation:", e)
        return False
    finally:
        # Закрытие соединения
        cursor.close()
        conn.close()