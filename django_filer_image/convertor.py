from __future__ import annotations
from io import BytesIO
from math import ceil
from PIL import Image


def get_image(file):
    image = Image.open(file)
    image = image.convert('RGB') if not image.mode == 'RGB' else image

    return image


def get_preview_image(image, preview_size, quality=100):
    size = get_preview_size(image, preview_size)
    resized_image = image.resize(size)

    preview_progressive_jpeg = get_jpeg(resized_image, progressive=False, quality=quality)

    return preview_progressive_jpeg


def get_preview_size(image, preview_size):
    preview_width, preview_height = preview_size

    if not preview_width and not preview_height:
        raise ValueError('Resize size is required.')

    original_width, original_height = image.size

    if preview_width and preview_height:
        resize_width = preview_width
        resize_height = preview_height
    elif preview_width:
        resize_width = preview_width
        resize_rate = preview_width / original_width
        resize_height = ceil(original_height * resize_rate)
    else:
        resize_height = preview_height
        resize_rate = preview_height / original_height
        resize_width = ceil(original_width * resize_rate)

    return resize_width, resize_height


def get_jpeg(image, progressive=True, quality=100):
    return convert_image(
        image,
        'JPEG',
        quality=quality,
        optimize=True,
        progressive=progressive,
    )


def get_webp(image, quality=1000):
    return convert_image(
        image,
        'WEBP',
        quality=quality,
        optimize=True,
    )


def convert_image(image, *args, **kwargs):
    blob_image = BytesIO()
    image.save(
        blob_image,
        *args,
        **kwargs
    )

    return blob_image
