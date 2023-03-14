from django import template
from songs.models import *

register = template.Library()

@register.simple_tag(name='getgenres')
def get_categories(filter=None):
    if not filter:
        return Genre.objects.all()
    else:
        return Genre.objects.filter(pk=filter)

@register.inclusion_tag('songs/list_genres.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Genre.objects.all()
    else:
        cats = Genre.objects.order_by(sort)

    return {"cats": cats, "cat_selected": cat_selected}
