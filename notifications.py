import json
import logging
import datetime
import asyncio

from aiogram import Bot

from parser.schedule import get_next_race
from utils import msk, ParallelTask
from settings import notification_template, race_week_notification_template


MOSCOW_TZ = datetime.timezone(datetime.timedelta(hours=3))


class Conditions:
    qualy_soon = False
    race_tomorrow = False
    race_soon = False
    race_week = False
    
    def __init__(self):
        self.next_race = get_next_race()

    def is_qualy_soon(self, now = datetime.datetime.now(MOSCOW_TZ)) -> bool:
        qualy = self.next_race['schedule']['qualy']
        qualy_date = datetime.date(*(int(i) for i in qualy['date'].split('-')))
        qualy_time = datetime.time(*(int(i) for i in qualy['time'][:-1].split(':')), tzinfo=MOSCOW_TZ)
        now_date = now.date()        
        now_time = now.timetz()

        if (now_date == qualy_date
            and (now + datetime.timedelta(hours=1)).timetz() >= qualy_time
            and not self.qualy_soon
        ):
            return True
        else:
            return False
    
    def is_race_tomorrow(self, now = datetime.datetime.now(MOSCOW_TZ)) -> bool:
        race = self.next_race['schedule']['race']
        race_date = datetime.date(*(int(i) for i in race['date'].split('-')))
        race_time = datetime.time(*(int(i) for i in race['time'][:-1].split(':')), tzinfo=MOSCOW_TZ)
        now_date = now.date()
        now_time = now.timetz()

        if ((now + datetime.timedelta(days=1)).date() == race_date
            and now_time >= race_time
            and not self.race_tomorrow
        ):
            return True
        else:
            return False

    def is_race_soon(self, now = datetime.datetime.now(MOSCOW_TZ)) -> bool:
        race = self.next_race['schedule']['race']
        race_date = datetime.date(*(int(i) for i in race['date'].split('-')))
        race_time = datetime.time(*(int(i) for i in race['time'][:-1].split(':')), tzinfo=MOSCOW_TZ)
        now_date = now.date()
        now_time = now.timetz()

        if (now_date == race_date
            and (now + datetime.timedelta(hours=1)).timetz() >= race_time
            and not self.race_soon
        ):
            return True
        else:
            return False
    
    def is_race_week(self, now = datetime.datetime.now(MOSCOW_TZ)) -> bool:
        race_date = datetime.date(*(int(i) for i in self.next_race['schedule']['race']['date'].split('-')))
        if race_date - datetime.timedelta(days=6) == now.date():
            return True
        else:
            return False

    @classmethod
    def drop_flags(cls):
        cls.qualy_soon = False
        cls.race_tomorrow = False
        cls.race_soon = False


async def send_notification(bot: Bot, when, what, name, time):
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


async def send_race_week_notification(bot: Bot, what):
    '''Присылает уведомление о начале гоночной недели'''

    with open('users.json', 'r', encoding= 'utf-8') as file:
        all_users_id = json.load(file)

    ans = race_week_notification_template.format(what)

    for user_id in all_users_id:
        try:
            await bot.send_message(user_id, ans, parse_mode='MarkdownV2')
        except Exception as e:
            logging.warning(f'Unable to send notification for user {user_id}: {e}')


async def notifier_loop(bot: Bot):
    '''Проверяет дату и время и вызывает отправление соответствующего уведомления'''

    run = True
    while run:
        conditions = Conditions()
        schedule = conditions.next_race['schedule']
        qualy_time_gen = (int(i) for i in schedule['qualy']['time'][:-1].split(':'))
        race_time_gen = (int(i) for i in schedule['race']['time'][:-1].split(':'))

        if conditions.is_qualy_soon():
            await send_notification(
                bot,
                'Скоро',
                'квалификация',
                conditions.next_race['name'],
                datetime.time(*qualy_time_gen, tzinfo=MOSCOW_TZ).strftime('%H:%M')
            )

            Conditions.qualy_soon = True
        
        elif conditions.is_race_tomorrow():
            await send_notification(
                bot,
                'Завтра',
                'гонка',
                conditions.next_race['name'],
                datetime.time(*race_time_gen, tzinfo=MOSCOW_TZ).strftime('%H:%M')
            )

            Conditions.race_tomorrow = True

        elif conditions.is_race_soon() and conditions.race_tomorrow:
            await send_notification(
                bot,
                'Скоро',
                'Гонка',
                conditions.next_race['name'],
                datetime.time(*race_time_gen, tzinfo=MOSCOW_TZ).strftime('%H:%M')
            )

            Conditions.race_soon = True
        
        if all([
            conditions.qualy_soon,
            conditions.race_tomorrow,
            conditions.race_soon
        ]):
            await asyncio.sleep(3600)
            conditions.drop_flags()
        else:
            await asyncio.sleep(600)


notifications_task = ParallelTask(notifier_loop)

if __name__ == '__main__':
    pass
