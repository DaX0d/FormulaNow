from types import NoneType
from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command

from settings import (
    next_race_ans,
    next_race_template,
    tracks,
    track_ans,
    track_template,
    DATE_FORMAT,
    TIME_FORMAT
)
from parser.schedule import get_next_race, get_next_track
from markups import home_markup
from utils import msk, translate_location, translate_session, tg_format


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

    return await message.answer(tg_format(ans), parse_mode='MarkdownV2', reply_markup=home_markup)


@next_race_router.message(Command('track'))
async def track_handler(message: Message):
    '''Отправляет информацию о треке, на котором следующая гонка'''

    next_race = get_next_race()
    next_track = get_next_track()

    if not (isinstance(next_track, NoneType) or isinstance(next_race, NoneType)):
        file_name = f'static/{tracks[next_race.loc['Country']
                                     if next_race.loc['Country'] not in ['United States', 'Spain']
                                     else next_race.loc['Location']]}'
        print(file_name)
        photo_file = FSInputFile(file_name)

        ans = track_ans + track_template.format(
            translate_location(next_race),
            next_track['circuit']['circuitName'],
            next_track['circuit']['city'],
            next_track['circuit']['circuitLength'][:-2] + ' м',
            next_track['laps'],
            next_track['circuit']['corners']
        )

        return await message.answer_photo(photo_file, parse_mode='MarkdownV2', caption=tg_format(ans), reply_markup=home_markup)
    else:
        return await message.answer('Пока что нет данных', parse_mode='MarkdownV2', reply_markup=home_markup)
