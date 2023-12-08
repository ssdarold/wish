# -*- coding: utf-8 -*-

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import logging
import sqlite3
import datetime
from datetime import date, timedelta
from aiogram.dispatcher import FSMContext
from functions.GetUserID import GetUserID
from functions.WhishListValidation import WhishListValidation
from functions.StringToListConverter import StringToListConverter
from functions.SetWishListItems import SetWishListItems
from functions.CheckUserRelation import CheckUserRelation
from functions.RelateUser import RelateUser
from functions.GetItemTitle import GetItemTitle
from aiogram.dispatcher.filters.state import State, StatesGroup
import qrcode
from aiogram.types import InputFile
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token="573458948:AAFKzIe-RW9Xf3nNWDeoq6THa6ZgovqkZL8")
dp = Dispatcher(bot, storage=MemoryStorage())

# ====== Базовые настройки =====

bot_name = "pryanebot"

# ====== Конец базовых настроек =====

# ====== Главное меню =====

show_related_button = types.InlineKeyboardButton(text="Мои друзья", callback_data="show_related")
show_events_button = types.InlineKeyboardButton(text="Мои события", callback_data="show_events")
create_wishlist_button = types.InlineKeyboardButton(text="Создать wish-лист", callback_data="create_whishlist")
invite_button = types.InlineKeyboardButton(text="Пригласить друга", callback_data="invite")
main_menu_button = types.InlineKeyboardButton(text="В главное меню", callback_data="main_menu")


# ====== Конец главного меню =====



# ======= Классы состояний ======

class YourStateMachine(StatesGroup):
    wishlist = State()
    update_wishlist = State()
    add_event_name = State()
    add_event_date = State()

# ======= Конец классов состояний ======


# def get_wishlist_data(user_id):
#     # Подключаемся к базе данных
#     conn = sqlite3.connect('db.sqlite3')
#     cursor = conn.cursor()

#     # Получаем inter_id
#     # inter_id = GetUserID(user_id)

#     # Получаем username
#     cursor.execute("SELECT username FROM main_user WHERE id=?", (user_id,))
#     username = cursor.fetchone()[0]

#     # Получаем wishlist_id
#     cursor.execute("SELECT id FROM main_whishlist WHERE owner_id=?", (user_id,))
#     wishlist_id = cursor.fetchone()[0]

#     # Получаем данные из main_whishlist_item
#     cursor.execute("SELECT Whish_list_item, Whish_list_title FROM main_whishlist_item WHERE Whish_list_id=?", (wishlist_id,))
#     wishlist_items = cursor.fetchall()

#     # Закрываем соединение с базой данных
#     conn.close()

#     return username, wishlist_items


# @dp.callback_query_handler(lambda c: c.data.startswith('showlist_'))
# async def show_wishlist(callback_query: types.CallbackQuery):
#     user_id = int(callback_query.data.split('_')[1])

#     username, wishlist_items = get_wishlist_data(user_id)

#     # Формируем сообщение
#     message_text = f"Wish-лист пользователя <b>{username}</b>:\n\n"
#     for index, item in enumerate(wishlist_items, start=1):
#         message_text += f"{index}. {item[0]}\n\n"

    
#     # Подключение к базе данных (замените на свой код подключения)
#     conn = sqlite3.connect('db.sqlite3')
#     cursor = conn.cursor()
    
#     # Проверка наличия wish-листа
#     cursor.execute("SELECT id FROM main_whishlist WHERE owner_id = ?", (user_id,))
#     list_id = cursor.fetchone()[0]

#     wlist_markup = types.InlineKeyboardMarkup()
#     wlist_markup.add(types.InlineKeyboardButton(text="Редактировать", callback_data=f"update_list_{list_id}"), main_menu_button)

#     # Отправляем сообщение
#     await bot.send_message(callback_query.from_user.id, message_text, parse_mode='HTML', reply_markup=wlist_markup)


@dp.callback_query_handler(lambda c: c.data.startswith('showlist_'))
async def show_wishlist(callback_query: types.CallbackQuery):
    try:
        # Получение user_id из callback_data
        user_id = int(callback_query.data.split('_')[1])

        # Подключение к базе данных
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        # Получение имени пользователя (username) из таблицы main_user
        cursor.execute("SELECT username FROM main_user WHERE id = ?", (user_id,))
        username = cursor.fetchone()[0]

        # Получение id списка из таблицы main_whishlist
        cursor.execute("SELECT id FROM main_whishlist WHERE owner_id = ?", (user_id,))
        wishlist_id = cursor.fetchone()[0]

        # Получение значений полей Whish_list_item и Whish_list_title из таблицы main_whishlist_item
        cursor.execute("SELECT Whish_list_item, Whish_list_title FROM main_whishlist_item WHERE Whish_list_id = ?", (wishlist_id,))
        whishlist_items = cursor.fetchall()

        # Формирование сообщения для ответа пользователю
        message_text = f"Wish-лист пользователя <b>{username}</b>:\n\n"
        for idx, item in enumerate(whishlist_items, start=1):
            item_text = f"{idx}. <a href=\"{item[0]}\">{item[1]}</a>\n"
            message_text += item_text

        # Получение id списка из таблицы main_whishlist для формирования кнопок
        cursor.execute("SELECT id FROM main_whishlist WHERE owner_id = ?", (user_id,))
        list_id = cursor.fetchone()[0]

        # Формирование кнопок
        keyboard = types.InlineKeyboardMarkup()
        edit_button = types.InlineKeyboardButton("Редактировать", callback_data=f"update_list_{list_id}")
        main_menu_button = types.InlineKeyboardButton("В главное меню", callback_data="main_menu")
        keyboard.add(edit_button, main_menu_button)

        # Отправка сообщения пользователю
        await bot.send_message(callback_query.from_user.id, message_text, reply_markup=keyboard, parse_mode='HTML')

    except Exception as e:
        # Обработка ошибок
        print(f"Error: {e}")

    finally:
        # Закрытие соединения с базой данных
        if conn:
            conn.close()



# Функция получения связанных пользователей
def get_related_users(user_id):
    # Подключаемся к базе данных
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Получаем inter_id
    inter_id = GetUserID(user_id)

    # Получаем связанных пользователей
    cursor.execute("SELECT second_user_id FROM main_relateduser WHERE first_user_id=?", (inter_id,))
    first_related_users = cursor.fetchall()

    cursor.execute("SELECT first_user_id FROM main_relateduser WHERE second_user_id=?", (inter_id,))
    second_related_users = cursor.fetchall()

    # Закрываем соединение с базой данных
    conn.close()

    return first_related_users + second_related_users

# Callback для показа друзей
@dp.callback_query_handler(lambda query: query.data == "show_related")
async def show_related_users(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    related_users = get_related_users(user_id)

    markup = types.InlineKeyboardMarkup()
    for related_user_id, in related_users:
        # Получаем username
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM main_user WHERE id=?", (related_user_id,))
        username = cursor.fetchone()[0]
        conn.close()

        # Формируем inline-кнопку
        button = types.InlineKeyboardButton(text=username, callback_data=f"showlist_{related_user_id}")
        markup.add(button)

    # Отправляем сообщение с кнопками
    await bot.send_message(user_id, "Выберите вашего друга для просмотра его wish-листа", reply_markup=markup)


# Callback для главного меню
@dp.callback_query_handler(lambda query: query.data == "main_menu")
async def show_related_users(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    inter_id = GetUserID(user_id)

    main_menu_markup = types.InlineKeyboardMarkup()
    main_menu_markup.add(types.InlineKeyboardButton(text="Мой wish-лист", callback_data="showlist_" + str(inter_id)), show_related_button, show_events_button, create_wishlist_button, invite_button)

    # Отправляем сообщение с кнопками
    await bot.send_message(user_id, "Главное меню", reply_markup=main_menu_markup)


# Callback для создания Wish-Листа
@dp.callback_query_handler(lambda c: c.data == 'create_whishlist')
async def create_wishlist(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    
    # Проверка наличия wish-листа
    owner_id = GetUserID(user_id)
    
    # Подключение к базе данных
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    # Проверка наличия wish-листа
    cursor.execute("SELECT id FROM main_whishlist WHERE owner_id = ?", (owner_id,))
    existing_wishlist = cursor.fetchone()
    
    if existing_wishlist:
        exist_list = types.InlineKeyboardMarkup()
        exist_list.add(types.InlineKeyboardButton(text="Просмотреть wish-лист", callback_data=f"showlist_{owner_id}"))
        # Если у пользователя уже есть wish-лист, отправляем сообщение об этом
        await bot.send_message(user_id, "У вас уже есть wish-лист!")
    else:
        # Если у пользователя нет wish-листа, начинаем состояние ожидания ввода ссылок
        await bot.send_message(user_id, "Для формирования wish-листа отправьте мне ссылки на новых строках.")
        await YourStateMachine.wishlist.set()

    # Закрытие соединения с базой данных
    conn.close()

# Логика создания листа
@dp.message_handler(state=YourStateMachine.wishlist)
async def process_wishlist(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    wishlist_text = message.text

    # Проверка формата ввода
    if WhishListValidation(wishlist_text):
        # Получаем id пользователя
        inter_id = GetUserID(user_id)

        # Подключаемся к базе данных
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        # Создаем новую запись в таблице main_whishlist
        creation_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO main_whishlist (creation_date, owner_id) VALUES (?, ?)", (creation_date, inter_id))
        conn.commit()

        # Получаем id добавленной записи
        cursor.execute("SELECT last_insert_rowid()")
        whishlist_id = cursor.fetchone()[0]

        # Преобразуем текст в список
        items = StringToListConverter(wishlist_text)

        # Вызываем функцию для добавления элементов в таблицу
        SetWishListItems(whishlist_id, items)

        wlist_markup = types.InlineKeyboardMarkup()
        wlist_markup.add(types.InlineKeyboardButton("Смотреть Wish-лист", callback_data="showlist_" + str(inter_id)), main_menu_button)
        await bot.send_message(user_id, "Wish-лист успешно создан!", reply_markup=wlist_markup)
        await state.finish()
    else:
        await bot.send_message(user_id, "Неверный формат ввода. Wish-лист должен содержать ссылки. Каждая ссылка должна начинаться с новой строки.")


# Обработчик обновления существующего whish-листа. Принимает на вход id листа.
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("update_list_"), state="*")
async def update_wishlist_callback(callback_query: types.CallbackQuery, state: FSMContext):
    whishlist_id = int(callback_query.data.split("_")[2])

    await state.update_data(whishlist_id=whishlist_id)
    await YourStateMachine.update_wishlist.set()

    await bot.send_message(callback_query.from_user.id, "Отправьте мне обновленные ссылки для wish-листа. Каждая ссылка с новой строки.")

# Логика обновления листа
@dp.message_handler(state=YourStateMachine.update_wishlist)
async def process_update_wishlist(message: types.Message, state: FSMContext):
    whishlist_id = (await state.get_data())["whishlist_id"]

    # Проверка формата ввода
    if WhishListValidation(message.text):

         # Подключение к базе данных
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        try:
            # Удаление записей из main_whishlist_item
            cursor.execute("DELETE FROM main_whishlist_item WHERE Whish_list_id = ?", (whishlist_id,))
            conn.commit()
        except sqlite3.Error as e:
            print("Error deleting wishlist items:", e)
        finally:
            # Закрываем соединение
            cursor.close()
            conn.close()

        # Получение списка из новых ссылок
        items = StringToListConverter(message.text)

        # Обновление базы данных с новыми данными
        SetWishListItems(whishlist_id, items)

        wlist_markup = types.InlineKeyboardMarkup()
        wlist_markup.add(types.InlineKeyboardButton("Смотреть Wish-лист", callback_data="showlist_" + str(GetUserID(message.from_user.id))), main_menu_button)
        await bot.send_message(message.from_user.id, "Wish-лист успешно обновлен!", reply_markup=wlist_markup)
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, "Неверный формат ввода. Wish-лист должен содержать ссылки. Каждая ссылка должна начинаться с новой строки.")


# Обработчик для команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message, state: FSMContext):
    try:
        # Подключение к базе данных
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        # Получение ID текущего пользователя в телеграм
        first_user_id = GetUserID(message.from_user.id)

        # Проверка наличия пользователя в таблице main_user
        cursor.execute("SELECT * FROM main_user WHERE tg_id = ?", (message.from_user.id,))
        user_exists = cursor.fetchone()

        if not user_exists:
            # Создание новой записи в таблице main_user
            cursor.execute("INSERT INTO main_user (username, tg_id, join_datetime) VALUES (?, ?, datetime('now'))",
                           (message.from_user.username, message.from_user.id))
            conn.commit()

        # Проверка наличия параметра start
        if message.get_args():
            second_user_id = GetUserID(message.get_args())
            if second_user_id:
                # Проверка наличия отношения между пользователями
                if not CheckUserRelation(first_user_id, second_user_id):
                    # Создание отношения между пользователями
                    RelateUser(first_user_id, second_user_id)

        # Проверка наличия записей в таблице main_whishlist
        cursor.execute("SELECT * FROM main_whishlist WHERE owner_id = ?", (first_user_id,))
        wishlist_exists = cursor.fetchone()

        # Создание клавиатуры
        start_markup = types.InlineKeyboardMarkup()

        if wishlist_exists:
            # Если есть записи в таблице main_whishlist, добавляем кнопку "Мой Whish-лист"
            start_markup.add(types.InlineKeyboardButton("Мой Wish-лист", callback_data="showlist_" + str(first_user_id)))
        else:
            # Если нет записей, добавляем кнопку "Создать Whish-лист"
            start_markup.add(types.InlineKeyboardButton("Создать Wish-лист", callback_data="create_whishlist"))

        # Получение текста приветствия из таблицы main_settings
        cursor.execute("SELECT start_message_text FROM main_settings")
        start_message_text = cursor.fetchone()[0]

        # Отправка приветственного сообщения
        await message.answer(start_message_text, reply_markup=start_markup, parse_mode="HTML")

    except sqlite3.Error as e:
        print("Error handling /start command:", e)
    finally:
        # Закрытие соединения
        cursor.close()
        conn.close()


# Обработчик для команды /help
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message, state: FSMContext):
    try:
        # Подключение к базе данных
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        # Получение текста справки из таблицы main_settings
        cursor.execute("SELECT help_message_text FROM main_settings")
        help_message_text = cursor.fetchone()[0]

        # Создание клавиатуры с кнопкой "В главное меню"
        help_markup = types.InlineKeyboardMarkup()
        help_markup.add(types.InlineKeyboardButton("В главное меню", callback_data="main_menu"))

        # Отправка сообщения с текстом справки и кнопкой "В главное меню"
        await message.answer(help_message_text, reply_markup=help_markup, parse_mode="HTML")

    except sqlite3.Error as e:
        print("Error handling /help command:", e)
    finally:
        # Закрытие соединения
        cursor.close()
        conn.close()

# Показать значимые события для пользователя
@dp.callback_query_handler(lambda query: query.data == "show_events")
async def show_events_handler(query: types.CallbackQuery, state: FSMContext):
    try:
        # Подключение к базе данных
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        # Получение id пользователя
        user_id = query.from_user.id

        # Получение id пользователя в базе данных
        inter_id = GetUserID(user_id)

        # Извлечение событий из базы данных
        cursor.execute("SELECT event_name, event_date FROM main_userevents WHERE user_id = ?", (inter_id,))
        events = cursor.fetchall()

        # Подготовка текста сообщения
        message_text = "Ваши важные события:\n"
        for i, (event_name, event_date) in enumerate(events, start=1):
            message_text += f"{i}. {event_name} - <b>{event_date}</b>\n\n"

        # Создание клавиатуры с кнопкой "В главное меню"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("В главное меню", callback_data="main_menu"))

        # Отправка сообщения с событиями и кнопкой "В главное меню"
        await bot.send_message(user_id, message_text, reply_markup=markup, parse_mode="HTML")

    except sqlite3.Error as e:
        print("Error handling show_events callback:", e)
    finally:
        # Закрытие соединения
        cursor.close()
        conn.close()

# Добавить пользовательское событие
@dp.callback_query_handler(lambda query: query.data == "add_event")
async def add_event_handler(query: types.CallbackQuery, state: FSMContext):
    user_id = query.from_user.id
    await bot.send_message(user_id, "Добавьте значимое для вас событие и я помогу о нем не забыть. Введите название события, например, 'День рождения дочки'.")

    # Активация состояния ожидания ввода названия события
    await YourStateMachine.add_event_name.set()

@dp.message_handler(state=YourStateMachine.add_event_name)
async def process_add_event_name(message: types.Message, state: FSMContext):
    try:
        # Сохранение в базу данных
        user_id = message.from_user.id
        inter_id = GetUserID(user_id)

        # Подключение к базе данных
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        # Создание новой записи в таблице main_userevents
        event_name = message.text
        cursor.execute("INSERT INTO main_userevents (user_id, event_name) VALUES (?, ?)", (inter_id, event_name))
        conn.commit()
        conn.close()

        # Отправка пользователю запроса на ввод даты события
        await bot.send_message(user_id, "Введите дату события, например, 24.01.")
        
        # Закончить состояние ожидания ввода названия события
        await state.finish()

        # Активация состояния ожидания ввода даты события
        await YourStateMachine.add_event_date.set()

    except sqlite3.Error as e:
        print("Error adding event name:", e)

@dp.message_handler(state=YourStateMachine.add_event_date)
async def process_add_event_date(message: types.Message, state: FSMContext):
    try:
        # Валидация формата даты
        date_format = "%d.%m"
        try:
            event_date = datetime.datetime.strptime(message.text, date_format).date()
        except ValueError:
            # Отправка сообщения об ошибке
            await bot.send_message(message.from_user.id, "Введен неверный формат даты. Дата события должна быть указана в формате 'ЧЧ.ММ', например, '24.01'. Повторите ввод.")
            return

        # Получение id пользователя
        user_id = message.from_user.id
        inter_id = GetUserID(user_id)

        # Подключение к базе данных
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        # Обновление записи в таблице main_userevents
        cursor.execute("UPDATE main_userevents SET event_date = ? WHERE user_id = ?", (event_date, inter_id))
        conn.commit()
        conn.close()

        # Создаем клавиатуру для возврата в галвное меню
        main_menu_mamarkup = types.InlineKeyboardMarkup()
        main_menu_mamarkup.add(types.InlineKeyboardButton(text="В главное меню", callback_data="main_menu"))

        # Отправка сообщения о успешном создании события
        await bot.send_message(user_id, "Поздравляю! Событие успешно создано.", reply_markup=main_menu_mamarkup)

        # Завершить состояние ожидания ввода даты события
        await state.finish()

    except sqlite3.Error as e:
        print("Error adding event date:", e)


# Callback-обработчик для приглашения друзей
@dp.callback_query_handler(lambda callback_query: callback_query.data == "invite")
async def invite_link(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    invite_link = f'https://t.me/{bot_name}?start={user_id}'
    filename = "site.png"
    # генерируем qr-код
    img = qrcode.make(invite_link)
    # сохраняем img в файл
    img.save(filename)
    image_url = InputFile(filename)
    await bot.send_photo(user_id, image_url, caption="QR-код для друзей.")
    await bot.send_message(user_id, f"""Отправьте эту ссылку или QR-код вашему другу и следите за Whish-листами друг друга.\n\nСсылка для друзей: {invite_link}.""", parse_mode="HTML")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)