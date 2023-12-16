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
from aiogram.utils.markdown import hbold, hcode

# bot = Bot(token="573458948:AAFKzIe-RW9Xf3nNWDeoq6THa6ZgovqkZL8")
bot = Bot(token="573458948:AAFKzIe-RW9Xf3nNWDeoq6THa6ZgovqkZL8")
dp = Dispatcher(bot, storage=MemoryStorage())

# ====== Базовые настройки =====

bot_name = "super_wish_bot"
db_path = "db.sqlite3"

# ====== Конец базовых настроек =====

# ====== Главное меню =====

create_wishlist_button = types.InlineKeyboardButton(text="Создать ВИШ-лист", callback_data="create_whishlist")
invite_button = types.InlineKeyboardButton(text="Пригласить друга", callback_data="invite")
find_user_button = types.InlineKeyboardButton(text="Найти пользователя", callback_data="find_user")
edit_list_button = types.InlineKeyboardButton(text="Редактировать", callback_data="update_list")
add_links_button = types.InlineKeyboardButton(text="Добавить ссылки", callback_data="add_links")
delete_links_button = types.InlineKeyboardButton(text="Удалить ссылки", callback_data="delete_links")
wish_list_ready_button = types.InlineKeyboardButton(text="ВИШ-лист готов", callback_data="main_menu")
bot_share_button = types.InlineKeyboardButton(text="Поделиться ботом", callback_data="invite")
show_my_list_button = types.InlineKeyboardButton(text="Смотреть ВИШ-лист", callback_data="show_mylist")
back_to_my_list_button = types.InlineKeyboardButton(text="Вернуться к моему ВИШ-листу", callback_data="show_mylist")
main_menu_button = types.InlineKeyboardButton(text="Меню", callback_data="main_menu")
next_button = types.InlineKeyboardButton(text="Отправил, что дальше?", callback_data="main_menu")


# ====== Конец главного меню =====



# ======= Классы состояний ======

class YourStateMachine(StatesGroup):
    wishlist = State()
    update_wishlist = State()
    add_event_name = State()
    add_event_date = State()
    add_find_user = State()
    add_links = State()

# ======= Конец классов состояний ======

# Функция для возврата виш-листа
async def show_wlist(inter_user_id: int, tg_id: int, self_list=False):
    # Подключаемся к базе данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Получаем значение столбца id в таблице main_whishlist
    cursor.execute("SELECT id FROM main_whishlist WHERE owner_id = ?", (inter_user_id,))
    whishlist_id = cursor.fetchone()

    # Получаем значение столбца id в таблице main_whishlist
    cursor.execute("SELECT create_list_image FROM main_settings WHERE id = 1")
    create_list_image = cursor.fetchone()[0]
    
    if not whishlist_id:
        await bot.send_message(inter_user_id, "У вас нет виш-листа.")
        return

    whishlist_id = whishlist_id[0]

    # Извлекаем все строки из таблицы main_whishlist_item
    cursor.execute("SELECT Whish_list_title, Whish_list_item FROM main_whishlist_item WHERE Whish_list_id = ?", (whishlist_id,))
    items = cursor.fetchall()

    # Получаем значение столбца username в таблице main_users
    cursor.execute("SELECT username FROM main_users WHERE id = ?", (inter_user_id,))
    username = cursor.fetchone()[0]

    # Формируем текстовое сообщение
    message_text = f'ВИШ-лист пользователя {username}\n\n'
    for i in range(10):
        if i < len(items):
            item = items[i]
            # Формируем текст в виде ссылки с HTML-разметкой
            link_text = f"{i + 1}. <a href=\"{item[1]}\">{item[0]}</a>"
        else:
            # Если элементов в списке не хватает, добавляем пустую строку
            link_text = f"{i + 1}."
        message_text += link_text + '\n'

    # Отправляем сообщение с Inline-кнопкой "В главное меню"
    keyboard = types.InlineKeyboardMarkup()
    main_menu_button = types.InlineKeyboardButton("В главное меню", callback_data="main_menu")
    if self_list:
        keyboard.add(edit_list_button)
        keyboard.add(wish_list_ready_button)
    else:
        keyboard.add(main_menu_button)

    # Отправляем сообщение с использованием parse_mode='HTML'
    create_list_photo = InputFile(create_list_image)

    # Если у пользователя нет wish-листа, начинаем состояние ожидания ввода ссылок
    await bot.send_photo(tg_id, create_list_photo, caption=message_text, reply_markup=keyboard, parse_mode="HTML")
    # await bot.send_message(tg_id, message_text, parse_mode=types.ParseMode.HTML, reply_markup=keyboard)

    # Закрываем соединение с базой данных
    conn.close()

# def get_wishlist_data(user_id):
#     # Подключаемся к базе данных
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     # Получаем inter_id
#     # inter_id = GetUserID(user_id)

#     # Получаем username
#     cursor.execute("SELECT username FROM main_users WHERE id=?", (user_id,))
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
#     conn = sqlite3.connect(db_path)
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
    # Получение user_id из callback_data
    tg_id = callback_query.from_user.id
    inter_user_id = int(callback_query.data.split('_')[1])
    await show_wlist(inter_user_id, tg_id)



    



# Функция получения связанных пользователей
def get_related_users(user_id):
    # Подключаемся к базе данных
    conn = sqlite3.connect(db_path)
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
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM main_users WHERE id=?", (related_user_id,))
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
    main_menu_markup.add(types.InlineKeyboardButton(text="Мой ВИШ-лист", callback_data="show_mylist"))
    main_menu_markup.add(create_wishlist_button)
    main_menu_markup.add(invite_button)
    main_menu_markup.add(find_user_button)

    # Отправляем сообщение с кнопками
    await bot.send_message(user_id, "Главное меню", reply_markup=main_menu_markup)



# Callback для главного меню
@dp.callback_query_handler(lambda query: query.data == "what_next")
async def what_next(callback_query: types.CallbackQuery):
    
    next_markup = types.InlineKeyboardMarkup()
    next_markup.add(invite_button, main_menu_button)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT whats_next_text FROM main_settings WHERE id=1")
    whats_next_text = cursor.fetchone()[0]
    conn.close()

    await bot.send_message(callback_query.from_user.id, whats_next_text, reply_markup=next_markup)


# Callback для показа собственного вишлиста
@dp.message_handler(commands=['show_mylist'])
@dp.callback_query_handler(lambda c: c.data == 'show_mylist')
async def show_mylist(callback_query: types.CallbackQuery, state: FSMContext):
    tg_id = callback_query.from_user.id
    
    # Проверка наличия wish-листа
    inter_user_id = GetUserID(tg_id)
    
    await show_wlist(inter_user_id, tg_id, self_list=True)


# Callback для поиска пользователя
@dp.message_handler(commands=['find_user'])
@dp.callback_query_handler(lambda c: c.data == 'find_user')
async def find_user(callback_query: types.CallbackQuery, state: FSMContext):
    tg_id = callback_query.from_user.id

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT find_user_text FROM main_settings WHERE id=1")
    second_related_users = cursor.fetchone()[0]

    conn.close()
    
    await bot.send_message(tg_id, second_related_users)
    await YourStateMachine.add_find_user.set()


# Логика для поиска пользователя
@dp.message_handler(state=YourStateMachine.add_find_user)
async def find_user(message: types.Message, state: FSMContext):

    # Получаем имя пользователя, чей вишлист нам нужно найти
    find_username = message.text

    # Подключение к базе данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Получаем внутренний ID пользователя по его юзернейму
    cursor.execute("SELECT COUNT(*) FROM main_users WHERE username = ?", (find_username,))
    found_user = cursor.fetchone()[0]

    if found_user:

        # Получаем внутренний ID пользователя по его юзернейму
        cursor.execute("SELECT id FROM main_users WHERE username = ?", (find_username,))
        inter_user_id = cursor.fetchone()[0]

        conn.close()

        await show_wlist(inter_user_id, message.from_user.id)
        await state.finish()

    else:
        not_find_markup = types.InlineKeyboardMarkup()
        not_find_markup.add(types.InlineKeyboardButton("Поделиться ботом", callback_data="invite"), types.InlineKeyboardButton("Вернуться к моему ВИШ-листу", callback_data="show_mylist"))

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT find_user_text FROM main_settings WHERE id=1")
        error_find_user_text = cursor.fetchone()[0]

        conn.close()

        await bot.send_message(message.from_user.id, error_find_user_text, reply_markup=not_find_markup)

        await state.finish()


# Callback для удаления ссылок
@dp.callback_query_handler(lambda c: c.data == 'delete_links')
async def delete_links(callback_query: types.CallbackQuery, state: FSMContext):
    tg_id = callback_query.from_user.id

    inter_id = GetUserID(tg_id)

    # Подключение к базе данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

     # Получаем ID вишлиста пользователя
    cursor.execute("SELECT id FROM main_whishlist WHERE owner_id = ?", (inter_id,))
    wishlist_id = cursor.fetchone()[0]

     # Получаем внутренний ID пользователя по его юзернейму
    cursor.execute("SELECT id, Whish_list_title FROM main_whishlist_item WHERE Whish_list_id = ?", (wishlist_id,))
    titles = cursor.fetchall()

    delete_markup = types.InlineKeyboardMarkup()

    for id, title in titles:
        delete_markup.add(types.InlineKeyboardButton(title, callback_data=f'delete_item_process_{id}'))

    delete_markup.add(types.InlineKeyboardButton("Отменить удаление", callback_data="main_menu"))

    await bot.send_message(tg_id, "Выберите элемент для удаления:", reply_markup=delete_markup)


# Диалог для подтверждения удаления ссылок
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("delete_item_process_"))
async def delete_links(callback_query: types.CallbackQuery, state: FSMContext):
    tg_id = callback_query.from_user.id

    id_item_for_delete = callback_query.data.split('_')[3]

    # Подключение к базе данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Получаем внутренний ID пользователя по его юзернейму
    cursor.execute("SELECT Whish_list_title FROM main_whishlist_item WHERE id = ?", (id_item_for_delete,))
    title_for_delete = cursor.fetchone()[0]

    confirm_markup = types.InlineKeyboardMarkup()
    confirm_markup.add(types.InlineKeyboardButton("Да", callback_data=f"del_it_{id_item_for_delete}"), types.InlineKeyboardButton("Нет", callback_data="main_menu"))

    await bot.send_message(tg_id, f"Вы уверены, что хотите удалить <b>{title_for_delete}</b> из своего ВИШ-листа?", reply_markup=confirm_markup, parse_mode="HTML")



# Логика для удаления ссылок
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("del_it_"))
async def delete_links(callback_query: types.CallbackQuery, state: FSMContext):
    tg_id = callback_query.from_user.id


    id_item_for_delete = callback_query.data.split('_')[2]
    
    # Подключение к базе данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Получаем ID вишлиста пользователя
    cursor.execute("DELETE FROM main_whishlist_item WHERE id = ?", (id_item_for_delete,))
    conn.commit()
    conn.close()

    success_del_markup = types.InlineKeyboardMarkup()
    success_del_markup.add(show_my_list_button, main_menu_button)

    await bot.send_message(tg_id, "Позиция удалена", reply_markup=success_del_markup)



# Callback для создания Wish-Листа
@dp.callback_query_handler(lambda c: c.data == 'create_whishlist')
async def create_wishlist(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    
    # Проверка наличия wish-листа
    owner_id = int(GetUserID(user_id))
    
    # Подключение к базе данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Проверка наличия wish-листа
    cursor.execute("SELECT COUNT(*) FROM main_whishlist WHERE owner_id = ?", (owner_id,))
    existing_wishlist = cursor.fetchone()[0]
    
    if existing_wishlist > 0:
        exist_list = types.InlineKeyboardMarkup()
        exist_list.add(types.InlineKeyboardButton(text="Просмотреть wish-лист", callback_data=f"showlist_{owner_id}"))
        # Если у пользователя уже есть wish-лист, отправляем сообщение об этом
        await bot.send_message(user_id, "У вас уже есть wish-лист!", reply_markup=exist_list)
    else:

        # Получение из базы текста
        cursor.execute("SELECT create_list_text FROM main_settings WHERE id = 1")
        create_list_text = cursor.fetchone()[0]

        cursor.execute("SELECT create_list_image FROM main_settings WHERE id = 1")
        create_list_image = cursor.fetchone()[0]

        # Если у пользователя нет wish-листа, начинаем состояние ожидания ввода ссылок
        await bot.send_message(user_id, create_list_text)

        # await bot.send_message(user_id, create_list_text)
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
        conn = sqlite3.connect(db_path)
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
        wlist_markup.add(show_my_list_button)
        wlist_markup.add(add_links_button)
        wlist_markup.add(wish_list_ready_button)

        # Получаем текст после создания вишлиста
        cursor.execute("SELECT after_create_list_text FROM main_settings WHERE id = 1")
        after_create_list_text = cursor.fetchone()[0]

        # Получаем текст после создания вишлиста
        cursor.execute("SELECT error_create_list_text FROM main_settings WHERE id = 1")
        error_create_list_text = cursor.fetchone()[0]

        await bot.send_message(user_id, after_create_list_text, reply_markup=wlist_markup)
        await state.finish()
    else:
        await bot.send_message(user_id, error_create_list_text)


# Callback для добавления ссылок
@dp.callback_query_handler(lambda c: c.data == 'add_links')
async def add_links(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    
    # Проверка наличия wish-листа
    owner_id = GetUserID(user_id)
    
    # Подключение к базе данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    

    # Если у пользователя нет wish-листа, начинаем состояние ожидания ввода ссылок
    await bot.send_message(user_id, "Вводи название желаемого подарка и добавляй ссылку на магазин. Каждый виш с новой строки.")
    await YourStateMachine.add_links.set()

    # Закрытие соединения с базой данных
    conn.close()


# Логика создания листа
@dp.message_handler(state=YourStateMachine.add_links)
async def process_addlinks(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    wishlist_text = message.text

    # Проверка формата ввода
    if WhishListValidation(wishlist_text):
        # Получаем id пользователя
        inter_id = GetUserID(user_id)

        # Подключаемся к базе данных
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Получаем id добавленной записи
        cursor.execute("SELECT id FROM main_whishlist WHERE owner_id = ?", (inter_id,))
        whishlist_id = cursor.fetchone()[0]

        # Преобразуем текст в список
        items = StringToListConverter(wishlist_text)

        # Вызываем функцию для добавления элементов в таблицу
        SetWishListItems(whishlist_id, items)

        wlist_markup = types.InlineKeyboardMarkup()
        wlist_markup.add(show_my_list_button)
        wlist_markup.add(add_links_button)
        wlist_markup.add(wish_list_ready_button)

        await bot.send_message(user_id, "Будут ещё ссылки или посмотрим твой ВИШ-лист?", reply_markup=wlist_markup)
        await state.finish()
    else:

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT error_create_list_text FROM main_settings WHERE id=1")
        error_create_list_text = cursor.fetchone()[0]
        conn.close()

        await bot.send_message(user_id, error_create_list_text)


# Обработчик обновления существующего whish-листа. Принимает на вход id листа.
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("update_list"), state="*")
async def update_wishlist_callback(callback_query: types.CallbackQuery, state: FSMContext):

    tg_id = callback_query.from_user.id

    update_markup = types.InlineKeyboardMarkup()
    update_markup.add(add_links_button)
    update_markup.add(delete_links_button)
    update_markup.add(wish_list_ready_button)

    await bot.send_message(tg_id, "Выберите опцию для редактирования", reply_markup=update_markup)

    # # Подключаемся к базе данных
    # conn = sqlite3.connect(db_path)
    # cursor = conn.cursor()

    # # Получаем InterID
    # cursor.execute("SELECT id FROM main_users WHERE tg_id = ?", (tg_id,))
    # inter_id = cursor.fetchone()[0]

    # # Получаем ID wish-листа
    # cursor.execute("SELECT id FROM main_whishlist WHERE owner_id = ?", (inter_id,))
    # whishlist_id = cursor.fetchone()[0]

    # conn.close()

    # await state.update_data(whishlist_id=whishlist_id)
    # await YourStateMachine.update_wishlist.set()

    # await bot.send_message(callback_query.from_user.id, "Отправьте мне обновленные ссылки для wish-листа. Каждая ссылка с новой строки.")

# Логика обновления листа
@dp.message_handler(state=YourStateMachine.update_wishlist)
async def process_update_wishlist(message: types.Message, state: FSMContext):
    whishlist_id = (await state.get_data())["whishlist_id"]

    # Проверка формата ввода
    if WhishListValidation(message.text):

         # Подключение к базе данных
        conn = sqlite3.connect(db_path)
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
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT error_create_list_text FROM main_settings WHERE id=1")
        error_create_list_text = cursor.fetchone()[0]
        conn.close()

        await bot.send_message(message.from_user.id, error_create_list_text)


# Обработчик для команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message, state: FSMContext):
    try:
        # Подключение к базе данных
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Получение ID текущего пользователя в телеграм
        first_user_id = GetUserID(message.from_user.id)

        # Проверка наличия пользователя в таблице main_users
        cursor.execute("SELECT * FROM main_users WHERE tg_id = ?", (message.from_user.id,))
        user_exists = cursor.fetchone()

        if not user_exists:
            # Создание новой записи в таблице main_users
            cursor.execute("INSERT INTO main_users (username, tg_id, join_datetime) VALUES (?, ?, datetime('now'))",
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
            start_markup.add(show_my_list_button)
            start_markup.add(invite_button)
            start_markup.add(find_user_button)
        else:
            # Если нет записей, добавляем кнопку "Создать Whish-лист"
            start_markup.add(create_wishlist_button)
            start_markup.add(invite_button)
            start_markup.add(find_user_button)

        # Получение текста приветствия из таблицы main_settings
        cursor.execute("SELECT start_message_text FROM main_settings WHERE id=1")
        start_message_text = cursor.fetchone()[0]

        # Получение картинки приветствия из таблицы main_settings
        cursor.execute("SELECT start_message_image FROM main_settings WHERE id=1")
        start_message_image = cursor.fetchone()[0]

        start_photo = InputFile(start_message_image)

        # Отправка приветственного сообщения
        # await message.answer(start_message_text, reply_markup=start_markup, parse_mode="HTML")
        await bot.send_photo(message.from_user.id, start_photo, caption=start_message_text, reply_markup=start_markup)

    except sqlite3.Error as e:
        print("Error handling /start command:", e)
    finally:
        # Закрытие соединения
        cursor.close()
        conn.close()


# Показать значимые события для пользователя
@dp.callback_query_handler(lambda query: query.data == "show_events")
async def show_events_handler(query: types.CallbackQuery, state: FSMContext):
    try:
        # Подключение к базе данных
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Получение id пользователя
        user_id = query.from_user.id

        # Получение id пользователя в базе данных
        inter_id = GetUserID(user_id)

        # Извлечение событий из базы данных
        cursor.execute("SELECT event_name, event_date FROM main_usersevents WHERE user_id = ?", (inter_id,))
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
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Создание новой записи в таблице main_usersevents
        event_name = message.text
        cursor.execute("INSERT INTO main_usersevents (user_id, event_name) VALUES (?, ?)", (inter_id, event_name))
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
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Обновление записи в таблице main_usersevents
        cursor.execute("UPDATE main_usersevents SET event_date = ? WHERE user_id = ?", (event_date, inter_id))
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
@dp.message_handler(commands=['invite'])
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
    invite_markup = types.InlineKeyboardMarkup()
    invite_markup.add(types.InlineKeyboardButton("Отправил, что дальше?", callback_data="what_next"))
    await bot.send_message(user_id, f"""{invite_link} - это твоя уникальная ссылка, отправь её другу, чтобы рассказать о ВИШе.""", reply_markup=invite_markup, parse_mode="HTML")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)