from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command

from settings import (
    next_race_ans,
    next_race_template,
    track_photoes,
    grand_prix_locations,
    track_ans,
    track_template
)
from parser.schedule import get_next_race
from markups import home_markup
from utils import msk, prev_date


next_race_router = Router(name='next_race')


@next_race_router.message(Command('next'))
async def next_race_handler(message: Message):
    '''Отправляет расписание следующей гонки'''

    ans = next_race_ans
    next_race = get_next_race()
    day, month = map(int, next_race['race_date'].split('.'))

    if next_race['schedule']['sprintRace']['time']:
        fp2_n = 'Квалификация к спринту'
        fp2_t = msk(next_race['schedule']['sprintQualy']['time'][:-4])
        fp3_n = 'Спринт'
        fp3_t = msk(next_race['schedule']['sprintRace']['time'][:-4])
    else:
        fp2_n = 'Практика 2'
        fp2_t = msk(next_race['schedule']['fp2']['time'][:-4])
        fp3_n = 'Практика 3'
        fp3_t = msk(next_race['schedule']['fp3']['time'][:-4])
    
    information = next_race_template.format(
        name=next_race['name'],
        fr_date='{:02d}\\.{:02d}'.format(*prev_date(day, month, 2)),
        sat_date='{:02d}\\.{:02d}'.format(*prev_date(day, month, 1)),
        sun_date='{:02d}\\.{:02d}'.format(day, month),
        fp1_t=msk(next_race['schedule']['fp1']['time'][:-4]),
        fp2_t=fp2_t,
        fp3_t=fp3_t,
        q_t=msk(next_race['schedule']['qualy']['time'][:-4]),
        r_t=msk(next_race['schedule']['race']['time'][:-4]),
        fp2_n=fp2_n,
        fp3_n=fp3_n
    )

    ans += information

    await message.answer(ans, parse_mode='MarkdownV2', reply_markup=home_markup)


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

    await message.answer_photo(photo_file, parse_mode='MarkdownV2', caption=ans, reply_markup=home_markup)
