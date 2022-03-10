import textwrap

from PIL import (
    Image,
    ImageDraw,
)

from ...assets import open_font
from ...settings import (
    FOOTER_SIZE,
    TITLE_FILL, LEFT_PADDING, CONTEXT_EXCERPT_FONT_SIZE, TITLE_WIDTH,
)


def create_context_footer_layer(excerpt: str) -> Image.Image:
    layer: Image.Image = Image.new('RGBA', FOOTER_SIZE)

    excerpt = '\n'.join(
        textwrap.wrap(
            excerpt,
            width=55,
            max_lines=2,
            placeholder='...',
        )
    )

    draw = ImageDraw.Draw(layer)
    draw.text(
        (LEFT_PADDING, 15),
        excerpt,
        font=open_font('Roboto-Regular.ttf', CONTEXT_EXCERPT_FONT_SIZE),
        fill=TITLE_FILL,
    )
    return layer
