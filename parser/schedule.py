import requests
import json
import datetime

from settings import grand_prix_locations


SCHEDULE_API = 'https://f1api.dev/api/current'
LAST_RACE_API = 'https://f1api.dev/api/current/last/race'
LAST_QUALY_API = 'https://f1api.dev/api/current/last/qualy'
LAST_SPRINT_API = 'https://f1api.dev/api/current/last/sprint/race'


# Парсеры
def parse_schedule():
    '''Запрашивает у API расписание текущего года и записывет его в файл schedule.json'''

    exc = requests.exceptions.ConnectionError('не удается получить расписание')

    api = requests.get(SCHEDULE_API)

    # Проверяем полученные данные (их должно быть много)
    if api.status_code == 200 and len(api.text.split(',')) > 10:
        with open('parser/data/schedule.json', 'w', encoding='utf-8') as file:
            data = json.loads(api.text)
            json.dump(data, file)
    else:
        raise exc


def parse_last_race():
    '''Парсит результаты последней гонки и записывает в файл last.json'''

    exc = requests.exceptions.ConnectionError

    race = requests.get(LAST_RACE_API)
    qualy = requests.get(LAST_QUALY_API)

    if race.status_code == 200 and len(race.text.split(',')) > 10:
        try:
            with open('parser/data/last.json', 'r', encoding='utf-8') as file:
                    data = json.load(file)
        except FileNotFoundError:
            data = {}
        except json.decoder.JSONDecodeError:
            data = {}

        data['race'] = json.loads(race.text)

        with open('parser/data/last.json', 'w', encoding='utf-8') as file:
            json.dump(data, file)
    else:
        raise exc
    
    if qualy.status_code == 200 and len(qualy.text.split(',')) > 10:
        try:
            with open('parser/data/last.json', 'r', encoding='utf-8') as file:
                    data = json.load(file)
        except FileNotFoundError:
            data = {}
        except json.decoder.JSONDecodeError:
            data = {}

        data['qualy'] = json.loads(qualy.text)

        with open('parser/data/last.json', 'w', encoding='utf-8') as file:
            json.dump(data, file)
    else:
        raise exc


# Геттеры
def get_schedule() -> list[dict]:
    '''Возвращает расписание в виде списка со словарями.

    Кажный словарь имеет структуру:
    {
        'id': race['round'] - 1,
        'name': grand_prix_locations[race['round'] - 1],
        'date': race['schedule']['race']['date'],
        'race_time': race['schedule']['race']['time'][:-4],
        'q_time': race['schedule']['qualy']['time'][:-4],
        'sq_time': race['schedule']['sprintQualy']['time'],
        'sprint_time': race['schedule']['sprintRace']['time']
    }
    '''

    with open('parser/data/schedule.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

        for race in data['races']:
            d = {
                'id': race['round'] - 1,
                'name': grand_prix_locations[race['round'] - 1],
                'date': race['schedule']['race']['date'],
                'race_time': race['schedule']['race']['time'][:-4],
                'q_time': race['schedule']['qualy']['time'][:-4],
                'sq_time': race['schedule']['sprintQualy']['time'],
                'sprint_time': race['schedule']['sprintRace']['time']
            }
        
    return d


def get_next_race() -> dict:
    '''Возвращает дынные о следующей гонке в виде словаря

    Структура словаря
    {
        'name': grand_prix_locations[race['round'] - 1],
        'race_date': race_date,
        'track': race['circuit'],
        'schedule': race['schedule'],
        'gp': race
    }
    '''
     
    now = datetime.datetime.now(datetime.timezone.utc)
    utc_offset = datetime.timedelta(hours=3)

    with open('parser/data/schedule.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

        for race in data['races']:
            race_dt_str = race['schedule']['race']['date'] + 'T' + race['schedule']['race']['time']  # 2025-06-01T13:00:00Z
            race_dt_utc = datetime.datetime.strptime(race_dt_str, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc)

            # Переводим в локальное время (UTC+3)
            race_dt_local = race_dt_utc + utc_offset

            if race_dt_local > now:
                ret = {
                    'name': grand_prix_locations[race['round'] - 1],
                    'race_date': '{}.{}'.format(race['schedule']['race']['date'][-2:], race['schedule']['race']['date'][5:7]),
                    'track': race['circuit'],
                    'schedule': race['schedule'],
                    'gp': race
                }

                return ret
    raise ValueError()


def get_last_race() -> dict:
    '''Возвращает результаты последней гонки'''

    with open('parser/data/last.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    return data['race']


def get_last_qualy() -> dict:
    '''Возвращает результаты последней квалификации'''

    with open('parser/data/last.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    return data['qualy']


if __name__ == '__main__':
    parse_last_race()
