from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse

# Create your views here.
def index(request):
    return HttpResponse("Страница приложения catalog.")

def categories(request, category_id):
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>Десерты по категории id {category_id} <h1>")

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
