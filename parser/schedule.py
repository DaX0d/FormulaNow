import requests
import json
import datetime
import fastf1.events

from settings import CURRENT_YEAR


API = 'https://f1api.dev/api/{}/{}'


def get_next_track():
    '''Возвращает информацию о треке'''

    next_event = get_next_race()

    response = requests.get(API.format(CURRENT_YEAR, next_event.loc['RoundNumber']))

    if response.status_code != 200:
        return None
    
    try:  
        data = json.loads(response.text)['race'][0]
        return data
    except:
        return None


def get_schedule():
    '''Возвращает расписание'''

    schedule = fastf1.events.get_event_schedule(CURRENT_YEAR, include_testing=False)

    return schedule


def get_next_race():
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
    pass
