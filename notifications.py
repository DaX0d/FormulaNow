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

MOSCOW_TZ = datetime.timezone(datetime.timedelta(hours=3))


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

    while True:
        next_race = get_next_race()

        now = datetime.datetime.now(MOSCOW_TZ)
        next_race = get_next_race()
        race_info = next_race['gp']

        race_utc = datetime.datetime.strptime(
            f"{race_info['schedule']['race']['date']}T{race_info['schedule']['race']['time']}",
            "%Y-%m-%dT%H:%M:%SZ"
        ).replace(tzinfo=datetime.timezone.utc)
        race_time = race_utc.astimezone(MOSCOW_TZ)

        qualy_utc = datetime.datetime.strptime(
            f"{race_info['schedule']['qualy']['date']}T{race_info['schedule']['qualy']['time']}",
            "%Y-%m-%dT%H:%M:%SZ"
        ).replace(tzinfo=datetime.timezone.utc)
        qualy_time = qualy_utc.astimezone(MOSCOW_TZ)

        # За день до гонки
        if (race_time.date() - datetime.timedelta(days=1) == now.date()
            and now.hour == 12
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
        elif (qualy_time - datetime.timedelta(hours=1) <= now < qualy_time
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
        elif (race_time - datetime.timedelta(hours=1) <= now < race_time
              and not race_soon_flag):

            race_soon_flag = True
            
            await send_notification(
                bot,
                'Гонка',
                'Скоро',
                next_race['name'],
                next_race['schedule']['race']['time'][:-4]
            )

        if now > race_time + datetime.timedelta(hours=2):
            race_next_day_flag = False
            race_soon_flag = False
            qualy_soon_flag = False
        
        await asyncio.sleep(600)


# if __name__ == '__main__':
#     asyncio.run(send_notification(bot, 'Гонка', 'Завтра', get_next_race()['name'], get_next_race()['schedule']['race']['time'][:-4]))
