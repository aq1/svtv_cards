from xml.etree import ElementTree

import requests
from django.conf import settings
from django.utils import timezone
from django.template.loader import render_to_string
from telegram import (
    Bot,
)

from project.celery import app
from ghost.ghost_admin_request import get_post
from ghost.ghost_admin_request import update_post


def get_rate(etree, currency):
    return round(float(etree.find(f"./Valute/CharCode[.='{currency}']/../Value").text.replace(',', '.')), 2)


@app.task
def update_rates():
    yesterday = timezone.now().strftime('%d/%m/%Y')
    cbr_yesterday = ElementTree.fromstring(
        requests.get(f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={yesterday}').text,
    )
    cbr = ElementTree.fromstring(
        requests.get('http://www.cbr.ru/scripts/XML_daily.asp').text,
    )
    crypto = requests.get('https://poloniex.com/public?command=returnTicker').json()

    usd_value = get_rate(cbr, 'USD')
    eur_value = get_rate(cbr, 'EUR')

    usd = {
        'value': usd_value,
        'down': (usd_value - get_rate(cbr_yesterday, 'USD') < 0)
    }

    eur = {
        'value': eur_value,
        'down': (eur_value - get_rate(cbr_yesterday, 'EUR') < 0)
    }

    btc = {
        'value': round((float(crypto['USDT_BTC']['lowestAsk']) + float(crypto['USDT_BTC']['highestBid'])) / 2),
        'down': float(crypto['USDT_BTC']['percentChange']) < 0,
    }

    context = {
        'usd': usd,
        'eur': eur,
        'btc': btc,
    }

    html = render_to_string(
        'currencies/currency_widget.html',
        context,
    )

    ghost_post = get_post(settings.GHOST_CURRENCY_POST_ID)
    update_post(
        post_id=settings.GHOST_CURRENCY_POST_ID,
        post_updated_at=ghost_post['updated_at'],
        data={
            'html': html,
        },
    )

    Bot(token=settings.TELEGRAM_TOKEN).send_message(
        settings.TELEGRAM_ADMIN_ID,
        text=f'Обновил курс валют\n{context}',
    )
