"""Streamfields live in here."""

from wagtail import blocks
from wagtail.templatetags.wagtailcore_tags import richtext
from wagtail.images.blocks import ImageChooserBlock
    
class LinkedImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True)
    link_url = blocks.URLBlock(required=False, help_text="Link to an external URL")
    link_page = blocks.PageChooserBlock(required=False, help_text="Link to an internal page")
    caption = blocks.CharBlock(required=False)

    class Meta:
        template = "streams/linked_image_block.html"
        icon = "image"
        label = "Linked Image"

class ButtonBlock(blocks.StructBlock):
    text = blocks.CharBlock(required=True, help_text="Text to display on the button")
    link_url = blocks.URLBlock(required=False, help_text="Link to an external URL")
    link_page = blocks.PageChooserBlock(required=False, help_text="Link to an internal page")
    
    style = blocks.ChoiceBlock(choices=[
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('warning', 'Warning'),
        ('danger', 'Danger'),
    ], default='primary', help_text="Bootstrap button style")
    
    alignment = blocks.ChoiceBlock(choices=[
        ('start', 'Left'),
        ('center', 'Center'),
        ('end', 'Right'),
    ], default='start', help_text="Button alignment")

    class Meta:
        template = "streams/button_block.html"
        icon = "placeholder"
        label = "Bootstrap Button"

class TitleAndTextBlock(blocks.StructBlock):
    """Title and text, nothing else"""

    title = blocks.CharBlock(required=True, help_text='Add your title')
    text = blocks.TextBlock(required=True, help_text='Add additional text')

    class Meta:
        template = "streams/title_and_text_blocks.html"
        icon = "edit"
        label = "Title & Text"

class CardBlock(blocks.StructBlock):
    """Cards with image and text and button(s)."""

    title = blocks.CharBlock(required=True, help_text="Add your title")

    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=True)),
                ("title", blocks.CharBlock(required=True, max_length=40)),
                ("text", blocks.TextBlock(required=True, max_length=200)),
                ("button_page", blocks.PageChooserBlock(required=False)),
                ("button_url", blocks.URLBlock(required=False, help_text="If the button page above is selected, that will be used first.")),
            ]
        )
    )

    class Meta:  # noqa
        template = "streams/card_block.html"
        icon = "placeholder"
        label = "SAGTA Cards"


class RichtextBlock(blocks.RichTextBlock):
    """Richtext with all the features."""

    class Meta:  # noqa
        template = "streams/richtext_block.html"
        icon = "doc-full"
        label = "Full RichText"


class SimpleRichtextBlock(blocks.RichTextBlock):
    """Richtext without (limited) all the features."""

    def __init__(
        self, required=True, help_text=None, editor="default", features=None, **kwargs
    ):  # noqa
        super().__init__(**kwargs)
        self.features = ["bold", "italic", "link"]

    class Meta:  # noqa
        template = "streams/richtext_block.html"
        icon = "edit"
        label = "Simple RichText"

class RawHTMLBlock(blocks.RawHTMLBlock):
    """Raw HTML block"""

    class Meta:
        icon = "code"
        label = "Raw HTML"

class CarouselBlock(blocks.StructBlock):
    images = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=True)),
            ]
        )
    )

    class Meta:
        template = "streams/carousel.html"
        icon = 'image'
        label = 'Carousel Image'