from django.db import models
from django.core.mail import send_mail
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
from wagtailcaptcha.models import WagtailCaptchaEmailForm

class FormField(AbstractFormField):
    page = ParentalKey(
        'ContactPage',
        on_delete=models.CASCADE,
        related_name='form_fields',
    )


class ContactPage(WagtailCaptchaEmailForm):

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
