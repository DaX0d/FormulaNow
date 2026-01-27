from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command

from settings import (
    next_race_ans,
    next_race_template,
    track_photoes,
    grand_prix_locations,
    track_ans,
    track_template,
    DATE_FORMAT,
    TIME_FORMAT
)
from parser.schedule import get_next_race
from markups import home_markup
from utils import msk, prev_date, translate_location, translate_session


next_race_router = Router(name='next_race')


@next_race_router.message(Command('next'))
async def next_race_handler(message: Message):
    '''Отправляет расписание следующей гонки'''

    ans = next_race_ans
    next_race = get_next_race()
    # day, month = map(int, next_race['race_date'].split('.'))
    
    information = next_race_template.format(
        name=translate_location(next_race),
        fr_date=next_race['Session1DateUtc'].strftime(DATE_FORMAT),
        sat_date=next_race['Session3DateUtc'].strftime(DATE_FORMAT),
        sun_date=next_race['Session5DateUtc'].strftime(DATE_FORMAT),
        fp1_t=msk(next_race['Session1DateUtc']).strftime(TIME_FORMAT),
        fp2_t=msk(next_race['Session2DateUtc']).strftime(TIME_FORMAT),
        fp3_t=msk(next_race['Session3DateUtc']).strftime(TIME_FORMAT),
        q_t=msk(next_race['Session4DateUtc']).strftime(TIME_FORMAT),
        r_t=msk(next_race['Session5DateUtc']).strftime(TIME_FORMAT),
        fp2_n=translate_session(next_race['Session2']),
        fp3_n=translate_session(next_race['Session3'])
    )

    ans += information

    return await message.answer(ans, parse_mode='MarkdownV2', reply_markup=home_markup)


@next_race_router.message(Command('track'))
async def track_handler(message: Message):
    '''Отправляет информацию о треке, на котором следующая гонка'''

    next_race = get_next_race()
    photo_file = FSInputFile(f'static/{track_photoes[grand_prix_locations.index(next_race['name'])]}.jpg')

    ans = track_ans + track_template.format(
        next_race['name'],
        next_race['track']['circuitName'],
        next_race['track']['city'],
        next_race['track']['circuitLength'][:-2] + ' м',
        next_race['gp']['laps'],
        next_race['track']['corners']
    )

    ans = ans.replace('-', '\\-')

    return await message.answer_photo(photo_file, parse_mode='MarkdownV2', caption=ans, reply_markup=home_markup)
