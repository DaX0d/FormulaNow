import requests
import json


def msk(t: str) -> str:
    '''Принимает время по гринвичу, возвращает по московскому времени'''
    h = (int(t[:2].lstrip('0') or '0') + 3) % 24
    return '{:02d}{}'.format(h, t[2:])


def prev_date(day, month, d) -> tuple[int, int]:
    '''Принимает дату (день и месяц), возвращает дату, отмотанную назад на указанное кол-во дней в виде кортежа'''

    if day - d > 0:
        return (day - d, month)
    
    new_month = month - 1

    if new_month - 1 < 8:
        match new_month % 2:
            case 0:
                return (day - d + 30, new_month)
            case 1:
                return (day - d + 31, new_month)
    else:
        match new_month % 2:
            case 0:
                return (day - d + 31, new_month)
            case 2:
                return (day - d + 30, new_month)


def try_open(filename: str):
    try:
        file = open(filename, 'r', encoding='utf-8')
    except FileNotFoundError:
        return False
    return True


def wrtite_to_json_from_page(page: requests.Response, filename: str, key: str):
    '''Проверяет статус страницы, если 200, то записывает в файл под введенным ключем, если 404, возвращает 404, иначе - ошибка'''

    exc = requests.exceptions.ConnectionError(f'unable to parse {key}')

    if page.status_code == 200 and len(page.text.split(',')) > 10:
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                    data = json.load(file)
        except FileNotFoundError:
            data = {}
        except json.decoder.JSONDecodeError:
            data = {}

        data[key] = json.loads(page.text)

        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file)
    elif json.loads(page.text)['status'] == 404:
        return 404
    else:
        raise exc
