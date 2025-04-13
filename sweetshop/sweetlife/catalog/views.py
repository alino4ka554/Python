from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from .models import Dessert, Category, TagDessert
from django.shortcuts import render
from django.urls import reverse

menu = [{'title': "О сайте", 'url_name': 'about'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'}
]

cats_db = [
 {'id': 1, 'name': 'Пирожные'},
 {'id': 2, 'name': 'Торты'},
 {'id': 3, 'name': 'Печенье'},
]


# Create your views here.
def index(request):
    data = {
        'title': '',
        'menu': menu,
        'cakes': Dessert.stocked.all(),
        'cat_selected': 0,
    }
    return render(request, 'catalog/index.html', context=data)

def about(request):
    return render(request, 'catalog/about.html', {'title': 'О сайте', 'menu': menu})

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")

def cake_detail(request, cake_slug):
    cake = get_object_or_404(Dessert, slug=cake_slug)
    data = {
        'title': cake.title,
        'menu': menu,
        'cake': cake,
        'cat_selected': 1,
    }
    return render(request, 'catalog/cake.html', context=data)

def show_tag_dessert(request, tag_slug):
    tag = get_object_or_404(TagDessert, slug=tag_slug)
    cakes = tag.tags.filter(in_stock=Dessert.Status.INSTOCK)
    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'cakes': cakes,
        'cat_selected': None,
    }
    return render(request, 'catalog/index.html', context=data)


def categories_by_slug(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    cakes = Dessert.stocked.filter(category_id=category.pk)
    data = {
        'title': category.name,
        'menu': menu,
        'cakes': cakes,
        'cat_selected': category.pk,
    }
    return render(request, 'catalog/index.html', context=data)


def dessert_detail(request, name):
    if name == 'eclair':
        url_redirect = reverse('index')
        return HttpResponseRedirect(url_redirect)
    return HttpResponse(f"<h1>Десерт {name} <h1>")

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
