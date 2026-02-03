from fastf1.ergast import Ergast

from settings import CURRENT_YEAR


ergast = Ergast()


def get_drivers():
    '''Возвращает таблицу с личным зачетом'''

    try:
        return ergast.get_driver_standings(CURRENT_YEAR).content[0]
    except IndexError:
        return None


def get_teams():
    '''Возвращает таблицу с кубком конструкторов'''
    
    try:
        return ergast.get_constructor_standings(CURRENT_YEAR).content[0]
    except IndexError:
        return None
