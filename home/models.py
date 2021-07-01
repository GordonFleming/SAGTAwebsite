from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core import blocks as streamfield_blocks

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
    )

    banner_title = models.CharField(max_length=100, blank=False, null=True)
    banner_subtitle = RichTextField(features=["bold","italic","h2","h3","h4"])
    banner_img_link = models.CharField(max_length=400, blank=False, null=True)
    banner_image = models.ForeignKey(
        "wagtailimages.Image", 
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    content_panels = Page.content_panels + [
        FieldPanel("banner_title"),
        FieldPanel("banner_subtitle"),
        FieldPanel("banner_img_link"),
        ImageChooserPanel("banner_image"),
        StreamFieldPanel("content"),
    ]

    class Meta:

        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"
