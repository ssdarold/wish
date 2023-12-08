import sqlite3


def SetWishListItems(wishlist_id, items):
    # Подключение к базе данных
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    try:
        # Перебор списка items
        for item in items:
            # Разделение элемента на имя и URL
            name, url = item[0], item[1]
            
            # Вставка записи в таблицу main_whishlist_item
            cursor.execute("INSERT INTO main_whishlist_item (Whish_list_id, Whish_list_title, Whish_list_item) VALUES (?, ?, ?)",
                           (wishlist_id, name, url))

        # Подтверждение изменений в базе данных
        conn.commit()

    
    finally:
        # Закрытие соединения
        conn.close()
        return True

