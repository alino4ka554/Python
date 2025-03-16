from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse

menu = [{'title': "О сайте", 'url_name': 'about'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'}
]

data_db = [
    {'id': 1, 'title': 'Заварное пирожное с Фисташковым кремом', 'content':
        'Нежное заварное пирожное с хрустящей корочкой, воздушным фисташковым кремом и свежими ягодами для яркого вкуса.', 
        'in_stock': True, 'image': 'catalog/images/fistashka.jpg'},
    {'id': 2, 'title': 'Пирожное Красный бархат', 'content':
        'Нежное пирожное «Красный бархат» с воздушным шоколадным бисквитом, пропитанным сливочным кремом, и легкими ванильными нотками.', 
        'in_stock': True, 'image': 'catalog/images/redbarhat.jpg'},
    {'id': 3, 'title': 'Печенье NY Cookies', 'content':
        'Американское домашнее печенье с колотым шоколадом или орешками.', 
        'in_stock': True, 'image': 'catalog/images/cookies.jpg'},
    {'id': 4, 'title': 'Пирожное Шоколадная Картошка', 'content':
        'Классическое пирожное «Шоколадная картошка» с насыщенным вкусом, покрытое мягким шоколадным ганашем.', 
        'in_stock': False, 'image': 'catalog/images/chocolate.jpg'},
    {'id': 5, 'title': 'Чизкейк Нью-Йорк с малиной', 'content':
        'Чизкейк «Нью-Йорк» с нежной сливочной текстурой на хрустящем корже, украшенный свежей малиной.', 
        'in_stock': True, 'image': 'catalog/images/ny.jpg'},
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
        'cakes': data_db
    }
    return render(request, 'catalog/index.html', context=data)

def about(request):
    return render(request, 'catalog/about.html', {'title': 'О сайте', 'menu': menu})

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")

def cake_detail(request, cake_id):
    return HttpResponse(f"Отображение пирожного с id = {cake_id}")

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
