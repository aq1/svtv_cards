import textwrap

from PIL import (
    Image,
    ImageDraw,
)

from ...assets import (
    open_image,
    open_font,
)
from ...settings import (
    CARD_WIDTH,
    FACTCHECKING_TITLE_LAYER_HEIGHT,
    FACTCHECKING_METER_SIZE,
    TITLE_FILL,
    LEFT_PADDING,
    FACTCHECKING_TITLE_TOP_PADDING,
    FACTCHECKING_TITLE_FONT_SIZE,
    FACTCHECKING_TITLE_WIDTH,
    FACTCHECKING_TITLE_MAX_LINES,
    FACTCHECKING_TITLE_SPACING,
    TITLE_PLACEHOLDER,
    FACTCHECKING_DATE_FONT_SIZE,
    FACTCHECKING_DATE_FILL,
)


def create_factchecking_title_layer(title: str, author_name: str, date: str, tag: str) -> Image.Image:
    meter = open_image(f'factchecking-status/{tag}.png').resize(FACTCHECKING_METER_SIZE)
    layer = Image.new('RGBA', (CARD_WIDTH, FACTCHECKING_TITLE_LAYER_HEIGHT))
    layer.alpha_composite(meter, (layer.width - meter.width, layer.height - meter.height))

    title = textwrap.wrap(
        title,
        width=FACTCHECKING_TITLE_WIDTH,
        max_lines=FACTCHECKING_TITLE_MAX_LINES,
        placeholder=TITLE_PLACEHOLDER,
    )

    title_font_size = FACTCHECKING_TITLE_FONT_SIZE + (FACTCHECKING_TITLE_MAX_LINES - len(title)) * 3

    title = '\n'.join(title)

    draw = ImageDraw.Draw(layer)
    draw.text(
        (LEFT_PADDING, FACTCHECKING_TITLE_TOP_PADDING),
        title,
        font=open_font('Roboto-Medium.ttf', title_font_size),
        fill=TITLE_FILL,
        spacing=FACTCHECKING_TITLE_SPACING,
    )

    author_name_y_coords = (
            FACTCHECKING_TITLE_LAYER_HEIGHT - 90 - FACTCHECKING_TITLE_FONT_SIZE - FACTCHECKING_DATE_FONT_SIZE
    )

    draw.text(
        (LEFT_PADDING, author_name_y_coords),
        author_name,
        font=open_font('Roboto-Medium.ttf', FACTCHECKING_TITLE_FONT_SIZE),
        fill=TITLE_FILL,
    )

    date_y_coord = author_name_y_coords + FACTCHECKING_TITLE_FONT_SIZE + FACTCHECKING_TITLE_SPACING
    draw.text(
        (LEFT_PADDING, date_y_coord),
        date,
        font=open_font('Roboto-Regular.ttf', FACTCHECKING_DATE_FONT_SIZE),
        fill=FACTCHECKING_DATE_FILL,
    )

    return layer
