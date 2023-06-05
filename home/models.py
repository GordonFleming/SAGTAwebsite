from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
# from wagtail.blocks import streamfield_blocks

from streams import blocks

class HomePage(Page):
    """Home page model."""

    template = "home/home_page.html"
    max_count = 1

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

    banner_title = models.CharField(max_length=100, blank=False, null=True)
    banner_subtitle = RichTextField(features=["bold","italic","h2","h3","h4"])
    banner_img_link = models.CharField(max_length=400, blank=False, null=True)
    notify_image = models.ForeignKey(
        "wagtailimages.Image", 
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    content_panels = Page.content_panels + [
        FieldPanel("banner_title"),
        FieldPanel("banner_subtitle"),
        FieldPanel("banner_img_link"),
        FieldPanel("notify_image"),
        FieldPanel("content"),
    ]

    class Meta:

        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"
