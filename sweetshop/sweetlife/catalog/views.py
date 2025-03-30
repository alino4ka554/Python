from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from .models import Dessert
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
        'cakes': Dessert.stocked.all()
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

def categories(request, category_id):
    data = {
        'title': cats_db[category_id-1]['name'],
        'menu': menu,
        'cakes': [],
        'cat_selected': category_id,
    }
    return render(request, 'catalog/index.html', context=data)

def categories_by_slug(request, category_slug):
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>Десерты по категории slug {category_slug} <h1>")

def dessert_detail(request, name):
    if name == 'eclair':
        url_redirect = reverse('index')
        return HttpResponseRedirect(url_redirect)
    return HttpResponse(f"<h1>Десерт {name} <h1>")

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
