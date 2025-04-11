import asyncio
import requests
from bs4 import BeautifulSoup
import json
import datetime

from settings import grand_prix_locations

SCHEDULE_API = 'https://f1api.dev/api/current'
SCHEDULE_URL = 'https://f-1world.ru/kalendar-gonok/8638-kalendar-jetapov-i-raspisanie-gonok-formuly-1-sezon-2025-goda.html'
DRIVERS_URL = 'https://f-1world.ru/turnirnaja-tablica/9324-formula-1-turnirnaja-tablica-pilotov-sezon-2025-goda.html'
TEAMS_URL = 'https://f-1world.ru/kubok-konstruktorov/9323-turnirnaja-tablica-kubka-konstruktorov-2025-goda.html'

_schedule: list[dict] = []
_next_track: dict = {}

async def parse_schedule():
    api = requests.get(SCHEDULE_API)
    try:
        with open('schedule.json', 'w', encoding='utf-8') as file:
            data = json.loads(api.text)
            json.dump(data, file)
    except requests.exceptions.ConnectionError:
        print('Не удалось установить соединение с API')

async def parse_standings():
    ...

async def parse_teams():
    ...

async def parse_all():
    global _schedule, _next_track
    await parse_schedule()
    _schedule = []

def get_schedule() -> list[dict]:
    global _schedule
    if not _schedule:
        with open('schedule.json', 'r', encoding='utf-8') as file:
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
    global _next_track
    if not _next_track:
        date = datetime.datetime.now().strftime('%d.%m')
        day, month = map(int, date.split('.'))
        with open('schedule.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            for race in data['races']:
                race_date = '{}.{}'.format(
                    race['schedule']['race']['date'][-2:],
                    race['schedule']['race']['date'][5:7]
                )
                race_day, race_month = map(int, race_date.split('.'))
                d = race_day - day + 30 * (race_month - month)
                if d >= 0:
                    ret = {
                        'name': grand_prix_locations[race['round'] - 1],
                        'race_date': race_date,
                        'track': race['circuit'],
                        'schedule': race['schedule']
                    }
                    _next_track = ret
                    return _next_track
        raise ValueError()
    return _next_track

if __name__ == '__main__':
    parse_all()
