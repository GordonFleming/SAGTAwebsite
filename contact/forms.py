from turnstile.fields import TurnstileField
from wagtail.contrib.forms.forms import FormBuilder

class WagtailTurnstileFormBuilder(FormBuilder):
    TURNSTILE_FIELD_NAME = 'turnstile'

    @property
    def formfields(self):
        # Add wagtailturnstile to formfields property
        fields = super(WagtailTurnstileFormBuilder, self).formfields
        fields[self.TURNSTILE_FIELD_NAME] = TurnstileField(theme='light')

        return fields
