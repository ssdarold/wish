import requests
from bs4 import BeautifulSoup

def GetItemTitle(url):
    try:
        # Отправляем GET-запрос по указанному URL
        response = requests.get(url)
        response.raise_for_status()  # Проверяем, успешно ли выполнен запрос

        # Используем BeautifulSoup для парсинга HTML-кода страницы
        soup = BeautifulSoup(response.text, 'html.parser')

        # Извлекаем значение тега <title>
        title = soup.title.string if soup.title else None

        return str(title) if title else None  # Приводим к типу string и возвращаем

    except Exception as e:
        # Обработка исключения и возврат None в случае ошибки
        print(f"Error getting item title: {e}")
        return None
