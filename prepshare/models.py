"""Prepshare page"""
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page

from streams import blocks

class PrepPage(Page):
    """Prepshare page class."""

    template = "prepshare/prepshare.html"
    filestash_link = models.CharField(max_length=200, blank=False)


    content_panels = Page.content_panels + [
        FieldPanel("filestash_link"),
    ]

    class Meta: # noqa
        verbose_name = "Prepshare Page"
        verbose_name_plural = "Prepshare Pages"
