import requests
import json
import datetime

from settings import grand_prix_locations


SCHEDULE_API = 'https://f1api.dev/api/current'
LAST_RACE_API = 'https://f1api.dev/api/current/last/race'
LAST_QUALY_API = 'https://f1api.dev/api/current/last/qualy'
LAST_SPRINT_API = 'https://f1api.dev/api/current/last/sprint/race'


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


if __name__ == '__main__':
    print(get_schedule())
