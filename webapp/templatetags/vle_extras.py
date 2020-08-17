from django import template
from django.conf import settings

from alumnica_model.models import Ambit

register = template.Library()


@register.simple_tag
def version_number():
    return settings.VERSION_NUMBER or 'NA'


@register.filter(name='split')
def split(value, arg):
    return value.split(arg)


@register.inclusion_tag('webapp/partials/partial_menu_list.html')
def get_menu():
    ambitos_list = Ambit.objects.filter(is_published=True)
    menu_list = [{'ambito': ambito,
                  'materias': ambito.subjects.all()}
                 for ambito in ambitos_list]
    return {'menu_list': menu_list}


@register.filter(name='learner_level')
def learner_level(value):
    level = int(value / 5000)
    if level < 1:
        level = 1

    if level > 3:
        level = 3
    return level


@register.simple_tag
def get_active_avatar(user, *args, **kwargs):
    if user and user.is_authenticated:
        learner = user.profile
        avatar = learner.avatar_progresses.filter(active=True).first()
        avatar_level = 3
        if avatar.points <= 50000:
            if avatar.points <= 15000:
                avatar_level = 1
            elif 15000 < avatar.points <= 50000:
                avatar_level = 2
        return {'avatar_name': avatar.avatar_name, 'avatar_level': avatar_level}
    else:
        return {}
