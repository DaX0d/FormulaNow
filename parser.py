import requests
from bs4 import BeautifulSoup
import json
from settings import grand_prix_locations

SCHEDULE_API = 'https://f1api.dev/api/current'
SCHEDULE_URL = 'https://f-1world.ru/kalendar-gonok/8638-kalendar-jetapov-i-raspisanie-gonok-formuly-1-sezon-2025-goda.html'
DRIVERS_URL = 'https://f-1world.ru/turnirnaja-tablica/9324-formula-1-turnirnaja-tablica-pilotov-sezon-2025-goda.html'
TEAMS_URL = 'https://f-1world.ru/kubok-konstruktorov/9323-turnirnaja-tablica-kubka-konstruktorov-2025-goda.html'

schedule: list[dict] = []

def parse_schedule():
    global schedule
    api = requests.get(SCHEDULE_API)
    try:
        with open('schedule.json', 'w', encoding='utf-8') as file:
            data = json.loads(api.text)
            json.dump(data, file)
            schedule = []
    except requests.exceptions.ConnectionError:
        print('Не удалось установить соединение с API')

def parse_standings():
    ...

def parse_teams():
    ...

def parse_all():
    ...

def get_schedule() -> list[dict]:
    global schedule
    if not schedule:
        with open('schedule.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            for race in data['races']:
                d = {
                    'name': grand_prix_locations[race['round'] - 1],
                    'date': race['schedule']['race']['date'],
                    'race_time': race['schedule']['race']['time'][:-4],
                    'q_time': race['schedule']['qualy']['time'][:-4],
                    'sq_time': race['schedule']['sprintQualy']['time'],
                    'sprint_time': race['schedule']['sprintRace']['time']
                }
                schedule.append(d)
    return schedule

if __name__ == '__main__':
    parse_schedule()
