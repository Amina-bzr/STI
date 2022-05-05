from django import template
from django.contrib.auth.models import Group

register = template.Library()

def has_group(user, nom_group):
    try:
        group =  Group.objects.get(name=nom_group)
    except Group.DoesNotExist:
        return False

    return (group in user.groups.all() or user.is_superuser)

register.filter('has_group', has_group)
