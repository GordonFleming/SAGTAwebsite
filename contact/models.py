from django.db import models
from datetime import date
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
)
from wagtail.fields import RichTextField
from wagtail.contrib.forms.models import (
    AbstractEmailForm,
    AbstractFormField,
)

from .forms import WagtailTurnstileFormBuilder
import re

class WagtailTurnstileEmailForm(AbstractEmailForm):
    """Pages implementing a turnstile form with email notification should inhert from this"""

    form_builder = WagtailTurnstileFormBuilder

    def process_form_submission(self, form):
        return super(WagtailTurnstileEmailForm, self).process_form_submission(form)

    class Meta:
        abstract = True

class FormField(AbstractFormField):
    page = ParentalKey(
        'ContactPage',
        on_delete=models.CASCADE,
        related_name='form_fields',
    )

class ContactPage(WagtailTurnstileEmailForm):

    template = "contact/contact_page.html"

    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    contact_img_link = models.CharField(max_length=400, blank=False, null=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', label='Form Fields'),
        FieldPanel('thank_you_text'),
        FieldPanel("contact_img_link"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel("subject"),
        ], "Email"),
    ]

    def render_email(self, form):
        # Get the original content (string)
        email_content = super().render_email(form)

        # Remove turnstile field from email
        email_content = re.sub(r"Turnstile:.*(\n|$)", "", email_content)

        # Add a title (not part of original method)
        title = '{}: {}'.format('Form', self.title)

        content = [title, '', email_content, '']

        # Add a link to the form page
        content.append('{}: {}'.format('Submitted Via', self.full_url))

        # Add the date the form was submitted
        submitted_date_str = date.today().strftime('%x')
        content.append('{}: {}'.format('Submitted on', submitted_date_str))

        # Content is joined with a new line to separate each text line
        content = '\n'.join(content)

        return content
