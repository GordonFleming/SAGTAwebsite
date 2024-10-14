from allauth.account.signals import user_signed_up
from django.contrib.auth.models import Group, User
from django.dispatch import receiver
from auth.adapter import is_valid_member

@receiver(user_signed_up)
def add_user_to_group(request, user, **kwargs):
    if is_valid_member(user.email):
        group = Group.objects.get(name='Members')
        user.groups.add(group)
        user.save()
