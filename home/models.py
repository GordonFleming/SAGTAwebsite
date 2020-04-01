from django.db import models

from wagtail.core.models import Page

class HomePage(Page):
    """Home page model."""
    templates = "home/home_page.html"
