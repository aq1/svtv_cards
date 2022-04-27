import datetime
from asyncio import sleep
import datetime as dt

import pytz
from pycoingecko import CoinGeckoAPI
from time import time

from requests import get

from config import db, msk
from main import Main

main = Main()
cg = CoinGeckoAPI()


def fix_currency(currency):
    if currency.lower() == 'btc':
        return 'bitcoin'
    elif currency.lower() == 'ltc':
        return 'litecoin'
    elif currency.lower() == 'eth':
        return 'ethereum'
    elif currency.lower() == 'bch':
        return 'bitcoin-cash'
    return currency


def convert_from_usd(amount: float, currency: str):
    currency = fix_currency(currency)
    curs = cg.get_price(ids=currency, vs_currencies='usd')
    if not curs:
        raise Exception("error while fetch curs")
    return round(amount / curs[currency]['usd'], 9)


async def check_transaction(wallet, user_id, amount, currency, level='', period='', comment=''):
    await sleep(0.5)
    currency = fix_currency(currency)
    start_time = time()
    while time() < start_time + 30 * 60:
        await sleep(60)
        resp = get(f"https://api.blockchair.com/{currency}/dashboards/address/{wallet}")
        if resp:
            transactions = resp.json()["data"][wallet]["transactions"]
            for x in transactions:
                trans_resp = get(f"https://api.blockchair.com/{currency}/dashboards/transaction/{x}")
                if trans_resp:
                    trans_meta = trans_resp.json()['data'][x]['transaction']
                    if dt.datetime.strptime(trans_meta["time"], "%Y-%m-%d %H:%M:%S").astimezone(msk) \
                            + dt.timedelta(hours=3) < dt.datetime.fromtimestamp(start_time, msk):
                        continue
                    outputs = trans_resp.json()['data'][x]['outputs']
                    for y in outputs:
                        if y['value'] / (10**8) == amount \
                                and y["recipient"] == wallet:
                            if level:
                                try:
                                    db.updateDB2(
                                        user_id,
                                        (amount, level, int(time()) + (60 * 60 * 24 * 30 * int(period)))
                                    )
                                    await main.success(user_id, level, period)
                                except Exception as e:
                                    main.log(f"{user_id} - smth went wrong: {e}", "check_transaction")
                            if comment:
                                await main.send_comment(user_id, comment, amount, currency)
                            db.updateDB_wallets((0, None, wallet))
                            main.log(f'{user_id}: success transaction,  wallet {wallet}, amount {amount} {currency} ',
                                     'check_transaction', 'INFO')
                            return
    db.updateDB_wallets((0, None, wallet))
    await main.expired(user_id, wallet)


async def activday2():
    users = db.selectDB_all_users_bot()
    if not users:
        return
    for user in users:
        id_telegram = user[0]
        if user[3] < time():
            db.deleteDB2(id_telegram)
            await main.kick(id_telegram)
            main.log(f'{id_telegram}: bye-bye', 'activday', 'INFO')
