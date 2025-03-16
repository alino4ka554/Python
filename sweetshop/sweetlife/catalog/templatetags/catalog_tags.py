from django import template
import catalog.views as views

register = template.Library()

@register.inclusion_tag('catalog/list_categories.html')
def show_categories(cat_selected=0):
    cats = views.cats_db
    return {"cats": cats, "cat_selected": cat_selected}