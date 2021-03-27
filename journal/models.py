"""Journal page"""
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core import blocks as streamfield_blocks

from streams import blocks

class JournalPage(Page):
    """Journal page class."""

    template = "journal/journal_page.html"
    
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
    )

    subtitle = models.CharField(max_length=100, null=True, blank = True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        StreamFieldPanel("content"),
    ]

    class Meta: # noqa
        verbose_name = "Journal Page"
        verbose_name_plural = "Journal Pages"