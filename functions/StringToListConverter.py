def StringToListConverter(text):
    # Разбиваем текст на строки
    lines = text.split('\n')
    
    # Создаем список для хранения результатов
    result_list = []
    
    # Обрабатываем каждую строку
    for line in lines:
        # Пропускаем пустые строки
        if not line.strip():
            continue
        
        # Находим позицию http/https
        http_index = line.find('http://')
        https_index = line.find('https://')
        
        # Определяем позицию разделителя
        separator_index = min(http_index, https_index) if http_index >= 0 and https_index >= 0 else max(http_index, https_index)
        
        # Разбиваем строку на две части: первая часть - имя, остальное - URL
        parts = [line[:separator_index].strip(), line[separator_index:].strip()] if separator_index >= 0 else [line.strip(), '']
        
        # Добавляем пару [имя, URL] в результат
        result_list.append(parts)
    
    return result_list




