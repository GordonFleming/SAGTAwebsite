from django.db import models
from datetime import date
from django.core.mail import send_mail

import os
from mailersend import emails
from dotenv import load_dotenv
load_dotenv()

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

    def send_mail(self, form):
        # Refer to https://docs.wagtail.org/en/stable/reference/contrib/forms/customisation.html#custom-send-mail-method
        # `self` is the FormPage, `form` is the form's POST data on submit

        # Email addresses are parsed from the FormPage's addresses field
        #addresses = [x.strip() for x in self.to_address.split(',')]

        # Subject
        submitted_date_str = date.today().strftime('%x')
        subject = f"{self.subject} - {submitted_date_str}"

        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        full_message_plain = 'From: {name} <{email}>\n\n{message}'.format(name=name, email=email, message=message)
        full_message_html = '<b>From:</b> {name} <br><b>Email:</b> {email} <br><b>Message:</b><br>{message}'.format(name=name, email=email, message=message)

        mailer = emails.NewEmail(os.environ.get('MAILERSEND_API_KEY'))
        
        mail_body = {}

        mail_from = {
            "name": "SAGTA Contact Form",
            "email": self.from_address,
        }

        recipients = [
            {
                "name": 'SAGTA',
                "email": self.to_address,
            }
        ]

        reply_to = {
            "name": name,
            "email": email,
        }

        mailer.set_mail_from(mail_from, mail_body)
        mailer.set_mail_to(recipients, mail_body)
        mailer.set_subject(subject, mail_body)
        mailer.set_html_content(full_message_html, mail_body)
        mailer.set_plaintext_content(full_message_plain, mail_body)
        mailer.set_reply_to(reply_to, mail_body)

        mailer.send(mail_body)
