import requests
import json


DRIVERS_URL = 'https://f1api.dev/api/current/drivers-championship'
TEAMS_URL = 'https://f1api.dev/api/current/constructors-championship'


def parse_drivers():
    '''Зарпашивает с API личный зачет F1 и сохранаяет'''
    exc = requests.exceptions.ConnectionError

    api_data = requests.get(DRIVERS_URL)

    if api_data.status_code == 200 and len(api_data.text.split(',')) > 10:
        try:
            with open('parser/data/standings.json', 'r', encoding='utf-8') as file:
                json_data = json.load(file)
        except FileNotFoundError:
            json_data = {}
        except json.JSONDecodeError:
            json_data = {}

        json_data['drivers'] = json.loads(api_data.text)

        with open('parser/data/standings.json', 'w', encoding='utf-8') as file:
            json.dump(json_data, file)
    else:
        raise exc


def parse_teams():
    '''Запрашивает с API кубок конструкторов и сохраняет'''
    exc = requests.exceptions.ConnectionError

    api_data = requests.get(DRIVERS_URL)

    if api_data.status_code == 200 and len(api_data.text.split(',')) > 10:
        try:
            with open('parser/data/standings.json', 'r', encoding='utf-8') as file:
                json_data = json.load(file)
        except FileNotFoundError:
            json_data = {}
        except json.JSONDecodeError:
            json_data = {}

        json_data['teams'] = json.loads(api_data.text)

        with open('parser/data/standings.json', 'w', encoding='utf-8') as file:
            json.dump(json_data, file)
    else:
        raise exc


def get_drivers() -> dict[str, int]:
    '''Возвращает словарь с личным зачетом'''
    pass


def get_teams() -> dict[str, int]:
    '''Возвращает словарь с кубком конструкторов'''
    pass
