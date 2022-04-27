import time
from datetime import datetime

from config import bot, chat_id, msk


class Main:
    def log(self, some_str_logs, name, level='ERROR'):
        with open("logs.txt", "a") as f:
            f.write(f"{datetime.now(msk).strftime('%Y-%m-%d %H:%M:%S')}. {name}: {level}: {some_str_logs}\n")

    def is_digit(string):
        if string.isdigit():
            return True
        else:
            try:
                float(string)
                return True
            except ValueError:
                return False

    async def create_link(self, user_name):
        try:
            link = await bot.create_chat_invite_link(chat_id, expire_date=time.time() + 3600, member_limit=1,
                                                     name=user_name)
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
                await bot.send_message(chat_id,
                                       f"Мне пришлось выгнать <a href='tg://user?id={id_telegram}'>{status['user']['first_name']}</a> за отсутствие подписки :(")
            await bot.send_message(id_telegram, f"К сожалению, Вы отменили подписку, поэтому мне "
                                                f"пришлось исключить Вас из чата. "
                                                f"\n\nПоддержите наше СМИ и приходите вновь!\n\nИспользуйте команду "
                                                f"/start для повторной авторизации в дальнейшем.", parse_mode='HTML')
        except Exception as e:
            self.log(str(e), 'kick')

    async def expired(self, user_id, wallet):
        await bot.send_message(user_id, f"Время ожидания платежа истекло, мы так и не получили его.\n\n"
                                        f"Если вы всё же отправляли средства на <code>{wallet}</code>, то обратитесь "
                                        f"в службу поддержки...")

    async def success(self, user_id, level, period):
        await bot.send_message(user_id, f"Поздравляю, ты оплатил(-а) подписку <strong>\"{level}\"</strong> "
                                        f"на <strong>{period} "
                                        f"месяц{'а' if period == '3' else ('ев' if period != '1' else '')}'</strong>, "
                                        f"теперь жми кнопку 🔐 Войти в чат...")

    async def send_comment(self, user_id, comment, amount, currency):
        await bot.send_message(chat_id, f"Донат-комментарий от <a href='tg://user?id={user_id}'>юзверя</a> "
                                        f"на сумму <strong>{amount} {currency}</strong>:\n\n"
                                        f"{comment}")
