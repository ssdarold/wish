import sqlite3

def RelateUser(first_user, second_user):
    try:
        # Подключение к базе данных
        conn = sqlite3.connect('./db.sqlite3')
        cursor = conn.cursor()

        # Запись связи между пользователями в таблицу main_relateduser
        cursor.execute("INSERT INTO main_relateduser (first_user_id, second_user_id) VALUES (?, ?)",
                       (first_user, second_user))

        # Сохранение изменений и закрытие соединения
        conn.commit()
        conn.close()

        return True  # Успешно создана связь между пользователями

    except Exception as e:
        # Обработка исключения и возврат False в случае ошибки
        print(f"Error relating users: {e}")
        return False