from datetime import datetime

import requests
from django.template.loader import render_to_string

from ghost.ghost_admin_request import get_page, update_page

URL = 'https://api.energyandcleanair.org/v1/russia_counter'
PAGE_ID = '6251dc7fd0120d00014c4052'


def update_gas_info():
    r = requests.get(URL)
    r.raise_for_status()

    data = r.json()
    date = datetime.strptime(data['date'].split(' ')[0], '%Y-%m-%d').strftime('%d.%m.%Y')
    total = round(data['total_eur'])
    oil = round(data['oil_eur'] / (10 ** 9), 3)
    gas = round(data['gas_eur'] / (10 ** 9), 3)
    coal = round(data['coal_eur'] / (10 ** 6))

    html = render_to_string(
        'currencies/gas_info.html',
        context={
            'date': date,
            'total': total,
            'oil': oil,
            'gas': gas,
            'coal': coal,
        },
    )

    page = get_page(PAGE_ID)

    update_page(
        page_id=PAGE_ID,
        page_updated_at=page['updated_at'],
        data={
            'html': html,
        }
    )
