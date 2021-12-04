from PIL.Image import Image


def compile_layers(background: Image, layers: list[Image]) -> Image:
    offset = 0

    for layer in layers:
        background.alpha_composite(layer, (0, offset))
        offset += layer.height

    return background.convert('RGB')
