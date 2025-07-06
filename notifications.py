import json
import logging
import datetime
import asyncio

from aiogram import Bot

from parser.schedule import get_next_race
from utils import msk
from settings import notification_template


MOSCOW_TZ = datetime.timezone(datetime.timedelta(hours=3))


class Conditions:
    qualy_soon = False
    race_tomorrow = False
    race_soon = False
    
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
            and not self.qualy_soon):
            return True
        else:
            return False
    
    def is_race_tomorrow(self, time: datetime.datetime) -> bool:
        pass

    def is_race_soon(self, time: datetime.datetime) -> bool:
        pass

    def drop_flags(self):
        self.qualy_soon = False
        self.race_tomorrow = False
        self.race_soon = False


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
    pass


if __name__ == '__main__':
    pass
