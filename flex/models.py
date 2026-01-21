"""Flexible page"""
from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from wagtail.fields import StreamField
# from wagtail import blocks as streamfield_blocks

from streams import blocks

class FlexPage(Page):
    """Flexible page class."""

    template = "flex/flex_page.html"

    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichtextBlock()),
            ("simple_richtext", blocks.SimpleRichtextBlock()),
            ("Raw_HTML", blocks.RawHTMLBlock()),
            ("cards", blocks.CardBlock()),
            ('carousel_image', blocks.CarouselBlock()),
        ],
        blank=True,
    )

    subtitle = models.CharField(max_length=100, null=True, blank = True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("content"),
    ]

    class Meta: # noqa
        verbose_name = "Flex Page"
        verbose_name_plural = "Flex Pages"
