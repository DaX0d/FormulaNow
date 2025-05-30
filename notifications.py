import json
import logging
import datetime
import asyncio

from aiogram import Bot

from parser import get_next_race
from utils import msk, prev_date
from settings import notification_template

# from main import bot


race_next_day_flag = False
race_soon_flag = False
qualy_soon_flag = False


async def send_notification(bot: Bot, what, when, name, time):
    '''Присылает уведомления о гонке всем зарегестрированным пользователям'''

    with open('users.json', 'r', encoding='utf-8') as file:
        all_users_id = json.load(file)

    ans = notification_template.format(
        when,
        what,
        name,
        msk(time)
    )

    ans = ans.replace('.', '\\.')
            
    for user_id in all_users_id:
        try:
            await bot.send_message(user_id, ans, parse_mode='MarkdownV2')
        except Exception as e:
            logging.warning(f'Unable to send notification for user {user_id}: {e}')


async def notifier_loop(bot: Bot):
    '''Проверяет дату и время и вызывает отправление соответствующего уведомления'''

    global race_next_day_flag, race_soon_flag, qualy_soon_flag

    next_race = get_next_race()
    date = datetime.datetime.now().strftime('%d.%m')
    day, month = map(int, date.split('.'))
    time = msk(datetime.datetime.now().strftime('%H'))

    while True:
        qualy_time = msk(next_race['schedule']['qualy']['time'])

        # За день до гонки
        if (prev_date(*map(int, next_race['race_date'].split('.')), d=1) == (day, month)
            and time == '12'
            and not race_next_day_flag):

            race_next_day_flag = True

            await send_notification(
                bot,
                'Гонка',
                'Завтра',
                next_race['name'],
                next_race['schedule']['race']['time'][:-4]
            )
        
        # За час до квалы
        elif (prev_date(*map(int, next_race['race_date'].split('.')), d=1) == (day, month)
            and time == str(int(qualy_time[:2]) - 1)
            and not qualy_soon_flag):

            qualy_soon_flag = True

            await send_notification(
                bot,
                'Квалификация',
                'Скоро',
                next_race['name'],
                next_race['schedule']['qualy']['time'][:-4]
            )
        
        # За час до гонки
        elif (next_race['race_date'] == '{:02d}{:02d}'.format(day, month)
            and time == str(int(msk(next_race['schedule']['race']['time'][:2])) - 1)
            and not race_soon_flag):

            race_soon_flag = True
            
            await send_notification(
                bot,
                'Гонка',
                'Скоро',
                next_race['name'],
                next_race['schedule']['race']['time'][:-4]
            )

        if all((race_next_day_flag, race_soon_flag, qualy_soon_flag)):
            await asyncio.sleep(10800)

            race_next_day_flag = False
            race_soon_flag = False
            qualy_soon_flag = False
        
        await asyncio.sleep(600)


# if __name__ == '__main__':
#     asyncio.run(send_notification(bot, 'Гонка', 'Завтра', get_next_race()['name'], get_next_race()['schedule']['race']['time'][:-4]))
