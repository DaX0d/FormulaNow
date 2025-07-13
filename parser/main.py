from os import makedirs
import asyncio
import requests
import logging

from .schedule import (
    parse_schedule,
    parse_last_race,
    parse_last_qualy,
    parse_last_sprint,
    parse_last_sprint_qualy
)
from .standings import (
    parse_drivers,
    parse_teams
)
from settings import PARSE_DELAY
from utils import ParallelTask


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
        if parse_last_qualy() == 404:
            logging.warning('unable to parse last qualy')
    except exc:
        logging.warning('unable to parse last qualy')

    try:
        if parse_last_sprint() == 404:
            logging.warning('unable to parse last sprint')
    except exc:
        logging.warning('unable to parse last sprint')
    
    try:
        if parse_last_sprint_qualy() == 404:
            logging.warning('unable to parse last sprint qualy')
    except exc:
        logging.warning('unable to parse last sprint qualy')

    try:
        parse_drivers()
    except exc:
        logging.warning('unable to parse drivers')

    try:
        parse_teams()
    except exc:
        logging.warning('unable to parse teams')


async def parser_loop():
    while True:
        parse_all()
        await asyncio.sleep(PARSE_DELAY)


parser_task = ParallelTask(parser_loop)

if __name__ == '__main__':
    parse_all()
