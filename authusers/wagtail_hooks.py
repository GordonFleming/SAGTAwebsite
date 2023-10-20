from django.urls import path, reverse
from wagtail import hooks
from wagtail.admin.menu import MenuItem

# from .views import index
# @hooks.register('register_admin_urls')
# def register_authusers_url():
#     return [
#         path('authusers/', index, name='check'),
#     ]

@hooks.register('register_admin_menu_item')
def register_check_menu_item():
    return MenuItem('Check', reverse('check'), icon_name='repeat')
