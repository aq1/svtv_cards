from pathlib import Path

from PIL import ImageFont, Image

ASSETS_DIR = Path(__file__).resolve().parent


def open_font(font_name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(
        str(ASSETS_DIR / 'fonts' / font_name),
        size=size,
    )


def open_image(name: str) -> Image.Image:
    return Image.open(
        str(ASSETS_DIR / 'images' / name)
    )
