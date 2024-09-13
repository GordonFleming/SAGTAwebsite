from wagtail.images.formats import Format, register_image_format
from django.utils.translation import gettext_lazy as _

# Additional custom formats
register_image_format(
    Format("responsive", _("Responsive"), "img-fluid", "width-800")
)

register_image_format(
    Format("center", _("Center"), "mx-auto d-block img-fluid", "width-800")
)