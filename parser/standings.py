import requests
import json

from settings import drivers_shortname_rus, teams_names_dict


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

    api_data = requests.get(TEAMS_URL)

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
    
    drivers_dict = {}

    with open('parser/data/standings.json', 'r', encoding='utf-8') as file:
        drivers_data: dict = json.load(file)['drivers']
    
    for driver in drivers_data['drivers_championship']:
        sname = driver['driver']['shortName']
        team_id = driver['teamId']

        drivers_dict[drivers_shortname_rus[sname] + f' \\({teams_names_dict[team_id]}\\)'] = driver['points']
    
    return drivers_dict


def get_teams() -> dict[str, int]:
    '''Возвращает словарь с кубком конструкторов'''
    
    teams_dict = {}

    with open('parser/data/standings.json', 'r', encoding='utf-8') as file:
        teams_data: dict = json.load(file)['teams']

    for team in teams_data['constructors_championship']:
        team_id = team['teamId']

        teams_dict[teams_names_dict[team_id]] = team['points']
    
    return teams_dict
