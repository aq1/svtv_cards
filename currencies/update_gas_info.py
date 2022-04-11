import io
import os
from datetime import datetime
from pathlib import Path
from xml.dom import minidom
from xml.dom.minidom import Element, Text

import requests
from PIL import Image
from cairosvg import svg2png
from django.contrib.humanize.templatetags.humanize import intcomma
from django.template.loader import render_to_string

from ghost.ghost_admin_request import get_page, upload_image, update_page

URL = 'https://api.energyandcleanair.org/v1/russia_counter'
PAGE_ID = '6251dc7fd0120d00014c4052'


def replace_text(node: Element, date, total):
    if isinstance(node, Text):
        node.nodeValue = node.nodeValue.replace('{date}', str(date)).replace('{total}', str(total))

    for child in node.childNodes:
        replace_text(child, date, total)


def generate_preview(date, total):
    with open(Path(os.path.dirname(__file__)) / 'static' / 'gas.svg') as f:
        doc = minidom.parseString(f.read())

    replace_text(doc, date, total)
    img_file = io.BytesIO()
    svg2png(doc.toxml(), write_to=img_file)
    img_file.seek(0)
    Image.open(img_file).convert('RGB').save(img_file, format='jpeg')
    image = Image.open(img_file)

    return upload_image(
        f'gas_info.jpg',
        image,
    ).json()['images'][0]['url']


def update_gas_info():
    r = requests.get(URL)
    r.raise_for_status()

    data = r.json()
    date = datetime.strptime(data['date'].split(' ')[0], '%Y-%m-%d').strftime('%d.%m.%Y')
    total = intcomma(round(data['total_eur']), use_l10n=False)
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

    preview = generate_preview(date, total)

    page = get_page(PAGE_ID)
    desc = 'Европа заплатила Путину за ворованный российский газ, спонсируя путинскую войну.'
    title = f'{total} евро'
    update_page(
        page_id=PAGE_ID,
        page_updated_at=page['updated_at'],
        data={
            'html': html,
            'twitter_image': preview,
            'og_image': preview,
            'og_title': title,
            'og_description': desc,
            'twitter_title': title,
            'twitter_description': desc,
        }
    )


if __name__ == '__main__':
    update_gas_info()
