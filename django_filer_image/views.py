from __future__ import annotations
from filer.fields.multistorage_file import MultiStorageFileField
from filer.models.abstract import BaseImage
from django.template.loader import get_template
from django.utils.html import mark_safe
from typing import TYPE_CHECKING

from .settings import (
    BREAKPOINTS,
    RATES,
)

if TYPE_CHECKING:
    from django.template import Template


class ProgressiveImage(BaseImage):
    webp = MultiStorageFileField(
        verbose_name='WebP изображение',
        null=True,
        blank=True,
        max_length=255,
    )
    progressive_jpeg = MultiStorageFileField(
        verbose_name='Progressive jpeg',
        null=True,
        blank=True,
        max_length=255,
    )
    preview = MultiStorageFileField(
        verbose_name='Progressive jpeg превью изображение',
        null=True,
        blank=True,
        max_length=255,
    )

    def render_image(self, breakpoints=None, rates=None, class_='', alt=''):
        template: Template = get_template('images/image.html.j2')
        context = {
            'image': self,
            'breakpoints': breakpoints or BREAKPOINTS,
            'rates': rates or RATES,
            'class': class_,
            'alt': alt,
        }

        html = template.render(context)

        return mark_safe(html)

    class Meta(BaseImage.Meta):
        app_label = 'images'
