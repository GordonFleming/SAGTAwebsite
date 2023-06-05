"""Journal page"""
from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from wagtail.fields import StreamField
# from wagtail import blocks as streamfield_blocks

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
	    use_json_field=True,
    )

    subtitle = models.CharField(max_length=100, null=True, blank = True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("content"),
    ]

    class Meta: # noqa
        verbose_name = "Journal Page"
        verbose_name_plural = "Journal Pages"
