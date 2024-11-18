from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Role
def create_default_roles(sender, **kwargs):
    roles = ['user', 'admin']
    for role_name in roles:
        Role.objects.get_or_create(name=role_name)