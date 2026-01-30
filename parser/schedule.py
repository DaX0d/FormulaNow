import requests
import json
import datetime
import fastf1.events

from settings import grand_prix_locations, CURRENT_YEAR
from utils import write_to_json_from_page


SCHEDULE_API = 'https://f1api.dev/api/current'
LAST_RACE_API = 'https://f1api.dev/api/current/last/race'
LAST_QUALY_API = 'https://f1api.dev/api/current/last/qualy'
LAST_SPRINT_API = 'https://f1api.dev/api/current/last/sprint/race'
LAST_SPRINT_QUALY_API = 'https://f1api.dev/api/current/last/sprint/qualy'


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

    race = requests.get(LAST_RACE_API)
    return write_to_json_from_page(race, 'parser/data/last.json', 'race')


def parse_last_qualy():
    '''Парсит результаты последней квалификации и записывает в файл last.json'''

    qualy = requests.get(LAST_QUALY_API)
    return write_to_json_from_page(qualy, 'parser/data/last.json', 'qualy')


def parse_last_sprint():
    '''Парсит результаты последнего спринта и записавает в файл last.json'''

    sprint = requests.get(LAST_SPRINT_API)
    return write_to_json_from_page(sprint, 'parser/data/last.json', 'sprint')


def parse_last_sprint_qualy():
    '''Парсит результаты последней спринт квалификации и записывает в файл last.json'''

    s_qualy = requests.get(LAST_SPRINT_QUALY_API)
    return write_to_json_from_page(s_qualy, 'parser/data/last.json', 's_qualy')


# Геттеры
def get_schedule():
    '''Возвращает расписание'''

    schedule = fastf1.events.get_event_schedule(CURRENT_YEAR, include_testing=False)

    return schedule


def get_next_race() -> dict:
    '''Возвращает дынные о следующей гонке'''
    
    return fastf1.events.get_events_remaining(datetime.datetime.now(), include_testing=False).iloc[0]


def get_last_event(session_num: int):
    schedule = fastf1.events.get_event_schedule(CURRENT_YEAR, include_testing=False)
    t_now = datetime.datetime.now()

    for i in range(len(schedule.index)-1, -1, -1):
        if schedule.iloc[i].loc[f'Session{session_num}DateUtc'] < t_now:
            return schedule.iloc[i]
    return None
    # return fastf1.events.get_event(2025, 23)


def get_last_race():
    '''Возвращает результаты последней гонки'''

    last_event = get_last_event(5)

    try:
        return last_event.get_race()
    except:
        return None


def get_last_qualy():
    '''Возвращает результаты последней квалификации'''

    last_event = get_last_event(4)

    try:
        return last_event.get_qualifying()
    except:
        return None


def get_last_sprint():
    '''Возвращает результаты последнего спринта'''

    last_event = get_last_event(3)

    try:
        return last_event.get_sprint()
    except:
        return None


def get_last_sprint_qualy():
    '''Возвращает разультаты последней спринт квалификации'''

    last_event = get_last_event(2)

    try:
        return last_event.get_sprint_qualifying()
    except:
        return None


if __name__ == '__main__':
    parse_last_race()
