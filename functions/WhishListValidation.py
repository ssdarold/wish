import re

def WhishListValidation(text):
    # Регулярное выражение для проверки формата текста
    pattern = r"^.+\shttps?://\S+$"
    
    # Разбиваем текст на строки и проверяем каждую строку
    lines = text.split('\n')
    
    for line in lines:
        # Проверка соответствия строки формату
        if not re.match(pattern, line):
            return False
    
    # Проверка, что каждый элемент начинается с новой строки
    if len(lines) > 1 and not lines[0]:
        return True
    
    return True


# Пример использования:
# input_text_valid = """Name1 http://example.com
# Name2 https://google.com
# Name3 http://stackoverflow.com
# Name4 https://invalid-url.com/section1/section2/section3
# Name5 https://invalid-url.com"""
# result_valid = WhishListValidation(input_text_valid)
# print(f"Validation Result (Valid): {result_valid}")

# input_text_invalid = """http://example.com
# ftp://invalid-url
# https://google.com
# https://invalid-url.com/section1/section2/section3
# invalid-url.com"""
# result_invalid = WhishListValidation(input_text_invalid)
# print(f"Validation Result (Invalid): {result_invalid}")
