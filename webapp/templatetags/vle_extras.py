from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def version_number():
    return settings.VERSION_NUMBER or 'NA'


@register.filter(name='split')
def split(value, arg):
    return value.split(arg)