from django.contrib import admin

# Register your models here.

from wagtail import hooks
from wagtail.admin.menu import MenuItem

@hooks.register('register_admin_menu_item')
def register_custom_menu_item():
    return MenuItem(
        'Users',  # Display name for the menu item
        '/admin/users/',  # URL for the "/admin/users" page
        icon_name='user',  # Name of the Wagtail icon to display
        name='users',  # A unique name for the menu item
        order=1000  # Position in the menu (optional, adjust as needed)
    )