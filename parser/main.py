from os import makedirs
import requests
import logging

from .schedule import (
    parse_schedule,
    parse_last_race
)
from .standings import (
    parse_drivers,
    parse_teams
)


exc = requests.exceptions.ConnectionError


def parse_all():
    makedirs('parser/data/', exist_ok=True)

    try:
        parse_schedule()
    except exc:
        logging.warning('unable to parse schedule')
    
    try:
        if parse_last_race() == 404:
            logging.warning('unable to parse last race')
    except exc:
        logging.warning('unable to parse last race')

    try:
        parse_drivers()
    except exc:
        logging.warning('unable to parse drivers')

    try:
        parse_teams()
    except exc:
        logging.warning('unable to parse teams')


if __name__ == '__main__':
    parse_all()
