from django import template
from django.db.models import Count
from catalog.models import Category, TagDessert


register = template.Library()

@register.inclusion_tag('catalog/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.annotate(
        total=Count("desserts")).filter(total__gt=0)
    return {"cats": cats, "cat_selected": cat_selected}


@register.inclusion_tag('catalog/list_tags.html')
def show_all_tags():
    return {"tags": TagDessert.objects.annotate(total=Count("tags"))
            .filter(total__gt=0)}
