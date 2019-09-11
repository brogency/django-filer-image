from os.path import splitext
from django.template.loader import get_template
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.html import mark_safe
from filer.fields.multistorage_file import MultiStorageFileField
from filer.models.abstract import BaseImage
from funcy import first

from .convertor import (
    get_image,
    get_jpeg,
    get_webp,
    get_preview_image,
)
from .settings import (
    BREAKPOINTS,
    RATES,
    IMAGE_QUALITY,
    IMAGE_CONSTANT_CSS_CLASS,
    IMAGE_CSS_CLASS,
    IMAGE_TEMPLATE,
    IMAGE_SRCSET_ATTRIBUTE,
    USES_WEBP,
    USES_PROGRESSIVE_JPEG,
    USES_PREVIEW,
    PREVIEW_SIZE,
)


class Image(BaseImage):
    webp = MultiStorageFileField(
        verbose_name='WebP image',
        null=True,
        blank=True,
        max_length=255,
    )
    progressive_jpeg = MultiStorageFileField(
        verbose_name='Progressive jpeg image',
        null=True,
        blank=True,
        max_length=255,
    )
    preview = MultiStorageFileField(
        verbose_name='Progressive jpeg preview image',
        null=True,
        blank=True,
        max_length=255,
    )

    def render_image(
            self,
            breakpoints=None,
            rates=None,
            class_=IMAGE_CSS_CLASS,
            alt='',
            template=IMAGE_TEMPLATE,
            srcset_attribute=IMAGE_SRCSET_ATTRIBUTE,
            **kwargs,
    ):
        template = get_template(template)
        context = {
            'image': self,
            'breakpoints': breakpoints or BREAKPOINTS,
            'rates': rates or RATES,
            'constant_class': IMAGE_CONSTANT_CSS_CLASS,
            'class': class_,
            'alt': alt,
            'srcset_attribute': srcset_attribute,
            'first': first,
            **kwargs,
        }

        html = template.render(context)

        return mark_safe(html)

    class Meta(BaseImage.Meta):
        app_label = 'images'


@receiver(pre_save, sender=Image)
def generate_images(sender, instance: Image, **kwargs):
    image = get_image(instance.file)
    filename = first(splitext(instance.file.name))

    if USES_PREVIEW:
        preview_image = get_preview_image(image, PREVIEW_SIZE)
        instance.preview.save(
            f'{filename}-preview.jpeg',
            preview_image,
            save=False,
        )

    if USES_PROGRESSIVE_JPEG:
        progressive_jpeg_image = get_jpeg(
            image,
            progressive=True,
            quality=IMAGE_QUALITY,
        )
        instance.progressive_jpeg.save(
            f'{filename}.jpeg',
            progressive_jpeg_image,
            save=False,
        )

    if USES_WEBP:
        webp_image = get_webp(
            image,
            quality=IMAGE_QUALITY,
        )
        instance.webp.save(
            f'{filename}.webp',
            webp_image,
            save=False,
        )
