from os import makedirs
import requests
from bs4 import BeautifulSoup
import json
import datetime
import logging
from datetime import timedelta

from settings import grand_prix_locations
from utils import prev_date


SCHEDULE_API = 'https://f1api.dev/api/current'
LAST_RACE_API = 'https://f1api.dev/api/current/last/race'
LAST_QUALY_API = 'https://f1api.dev/api/current/last/qualy'
LAST_SPRINT_API = 'https://f1api.dev/api/current/last/sprint/race'
DRIVERS_URL = 'https://f-1world.ru/turnirnaja-tablica/9324-formula-1-turnirnaja-tablica-pilotov-sezon-2025-goda.html'
TEAMS_URL = 'https://f-1world.ru/kubok-konstruktorov/9323-turnirnaja-tablica-kubka-konstruktorov-2025-goda.html'


_schedule: list[dict] = []
_next_track: dict = {}
_standings: dict = {}
_last_race: dict = {}
_last_qualy: dict = {}


def parse_schedule():
    '''Запрашивает у API расписание текущего года и записывет его в файл schedule.json'''

    api = requests.get(SCHEDULE_API)

    try:
        with open('data/schedule.json', 'w', encoding='utf-8') as file:
            data = json.loads(api.text)
            json.dump(data, file)
    except requests.exceptions.ConnectionError:
        logging.warning('Не удалось установить соединение с API')


def parse_standings():
    '''Парсит таблицу с сайта и записывает данные в standings.json с ключем "racers"'''

    global _standings

    page = requests.get(DRIVERS_URL)
    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.find('table')
    rows = table.find_all('tr')[1:]
    racers = {}

    for row in rows:
        name = '{} ({})'.format(row.find_all('td')[1].text.rstrip(' '), row.find_all('td')[2].text)
        points = row.find_all('td')[5].text
        racers[name] = int(points) if points else 0
    
    try:
        with open('data/standings.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
    except FileNotFoundError:
        data = {}
    except json.decoder.JSONDecodeError:
        data = {}

    data['racers'] = racers
    _standings['racers'] = racers

    with open('data/standings.json', 'w', encoding='utf-8') as file:
        json.dump(data, file)


def parse_teams():
    '''Парсит таблицу кубка конструкторов с сайта и записывает данные в standings.json с ключем "teams"'''

    global _standings

    page = requests.get(TEAMS_URL)
    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.find('table')
    rows = table.find_all('tr')[1:]
    teams = {}

    for row in rows:
        name = row.find_all('td')[1].text
        points = int(row.find_all('td')[4].text)
        teams[name] = points
    
    with open('data/standings.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    data['teams'] = teams
    _standings['teams'] = teams

    with open('data/standings.json', 'w', encoding='utf-8') as file:
        json.dump(data, file)


def parse_last_race():
    '''Парсит результаты последней гонки и записывает в файл last.json'''

    race = requests.get(LAST_RACE_API)
    qualy = requests.get(LAST_QUALY_API)

    if race.status_code == 200:
        try:
            try:
                with open('data/last.json', 'r', encoding='utf-8') as file:
                        data = json.load(file)
            except FileNotFoundError:
                data = {}
            except json.decoder.JSONDecodeError:
                data = {}

            data['race'] = json.loads(race.text)

            with open('data/last.json', 'w', encoding='utf-8') as file:
                json.dump(data, file)

        except requests.exceptions.ConnectionError:
            logging.warning('Не удалось установить соединение с API')
    
    if qualy.status_code == 200:
        try:
            try:
                with open('data/last.json', 'r', encoding='utf-8') as file:
                        data = json.load(file)
            except FileNotFoundError:
                data = {}
            except json.decoder.JSONDecodeError:
                data = {}

            data['qualy'] = json.loads(qualy.text)

            with open('data/last.json', 'w', encoding='utf-8') as file:
                json.dump(data, file)
                
        except requests.exceptions.ConnectionError:
            logging.warning('Не удалось установить соединение с API')


def parse_all():
    '''Вызывает парсеры расписания, личного зачета и кубка контсрукторов и чистит кеш'''

    global _schedule, _next_track, _standings

    makedirs('data', exist_ok=True)

    try:
        logging.info('Start parsing')

        parse_schedule()
        parse_standings()
        parse_teams()
        parse_last_race()

        _schedule = []
        _next_track = {}
        _last_race = {}

        logging.info('Parsing successfuly complited')
    except Exception as e:
        logging.warning(f'Парсинг не удался: {e}')


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
    global _schedule

    if not _schedule:
        with open('data/schedule.json', 'r', encoding='utf-8') as file:
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
                _schedule.append(d)

    return _schedule


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
    global _next_track

    if not _next_track:
        now = datetime.datetime.now(datetime.timezone.utc)
        utc_offset = timedelta(hours=3)

        with open('data/schedule.json', 'r', encoding='utf-8') as file:
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

                    _next_track = ret
                    return _next_track
        raise ValueError()
    return _next_track


def get_standings() -> dict:
    '''Возвращает словарь с расписанием'''

    global _standings

    if not _standings:
        with open('data/standings.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        _standings = data

    return _standings


def get_last_race() -> dict:
    '''Возвращает результаты последней гонки'''

    global _last_race

    if not _last_race:
        with open('data/last.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        _last_race = data['race']

    return _last_race


def get_last_qualy() -> dict:
    '''Возвращает результаты последней квалификации'''

    global _last_qualy

    if not _last_qualy:
        with open('data/last.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        _last_race = data['qualy']

    return _last_race


if __name__ == '__main__':
    parse_all()
