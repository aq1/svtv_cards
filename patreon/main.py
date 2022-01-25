from datetime import datetime
import time
import pytz

from config import bot, chat_id


class Main:
    def log(self, some_str_logs, name, level='ERROR'):
        with open("logs.txt", "a") as f:
            f.write(f"{datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M:%S')}. {name}: {level}: {some_str_logs}\n")

    async def create_link(self, user_name):
        try:
            link = await bot.create_chat_invite_link(chat_id, expire_date=time.time()+3600, member_limit=1, name=user_name)
            return link.invite_link
        except Exception as e:
            self.log(str(e), 'create_link')

    async def kick(self, id_telegram):
        try:
            status = await bot.get_chat_member(chat_id, id_telegram)
            if status['status'] == 'left' or status['status'] == 'kicked':
                print(f"{id_telegram} нет в чате. Доступ в чат для него закрыт")
            else:
                await bot.unban_chat_member(chat_id, id_telegram)
                await bot.send_message(chat_id, f"Мне пришлось выгнать <a href='tg://user?id={id_telegram}'>{status['user']['first_name']}</a> за отсутствие подписки :(")
            await bot.send_message(id_telegram, f"К сожалению, Вы отменили подписку на наш Patreon, поэтому мне "
                                                f"пришлось исключить Вас из чата. "
                                                f"\n\nПоддержите наше СМИ и приходите вновь!\n\nИспользуйте команду "
                                                f"/start для повторной авторизации в дальнейшем.", parse_mode='HTML')
        except Exception as e:
            self.log(str(e), 'kick')
