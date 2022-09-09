"""Flexible page"""
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core import blocks as streamfield_blocks

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
        ],
        null=True,
        blank=True,
	    use_json_field=True,
    )

    subtitle = models.CharField(max_length=100, null=True, blank = True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("content"),
    ]

    class Meta: # noqa
        verbose_name = "Flex Page"
        verbose_name_plural = "Flex Pages"
