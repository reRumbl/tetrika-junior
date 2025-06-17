import csv
from collections import defaultdict
import requests


def fetch_category_members(category: str, session: requests.Session) -> list[str]:
    '''Циклическое получение всех категорий с википедии'''
    URL = 'https://ru.wikipedia.org/w/api.php' 
    cmcontinue = None  # Параметр продолжения запросов
    titles = []  # Список с категориями

    while True:
        params = {
            'action': 'query',  # Действие (запрос)
            'list': 'categorymembers',  # Тип списка (категории)
            'cmtitle': f'Category:{category}',  # Текст запроса
            'cmlimit': '500',  # Категорий за раз (500)
            'format': 'json'  # Формат (JSON)
        }
        if cmcontinue:  # Если есть еще данные
            params['cmcontinue'] = cmcontinue  # Продолжение запросов

        response = session.get(URL, params=params)  # GET запрос википидеии с параметрами, указанными выше
        data = response.json()  # Преобразование в JSON формат из объекта requests.Response
        members = data['query']['categorymembers']  # Получние словарей с категориями

        titles.extend(member['title'] for member in members)  # Расширение списка с названиями категорий

        if 'continue' not in data:  # Если закончились данные
            break  # Конец запросов
        cmcontinue = data['continue']['cmcontinue']  # Обновление параметра продолжения

    return titles


def count_first_letters(titles: list[str]) -> dict[str, int]:
    '''Подсчет первых букв из названий'''
    counts = defaultdict(int)  # Создание пустого словаря dict[str, int]
    for title in titles:
        if not title:
            continue
        first_char = title[0].upper()  # Получение первой буквы названия категории
        if 'А' <= first_char <= 'Я':  # Если буква из русского алфавита
            counts[first_char] += 1  # Увеличение счетчика для данной буквы в словаре
    return counts


def main():
    session = requests.Session()
    category = 'Животные по алфавиту'
    titles = fetch_category_members(category, session)
    counts = count_first_letters(titles)

    with open('task2/beasts.csv', 'w', newline='', encoding='utf-8') as csvfile:  # Открытие/Создание CSV файла
        writer = csv.writer(csvfile)  # Создание объекта для записи в CSV файл
        for letter in sorted(counts.keys()):
            writer.writerow([letter, counts[letter]])  # Построчная запись в CSV файл
            

if __name__ == '__main__':
    main()
