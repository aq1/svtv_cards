import io
from typing import Optional

import requests
from PIL import (
    Image,
)
from PIL.Image import Image as ImageType


def download_image(image_url: str) -> Optional[ImageType]:
    response = requests.get(image_url)
    if response.status_code != 200:
        return

    return Image.open(io.BytesIO(response.content))
