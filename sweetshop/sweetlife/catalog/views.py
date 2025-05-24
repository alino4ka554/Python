from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from .models import Dessert, Category, TagDessert
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
import uuid
from django.db import models
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .forms import AddDessertForm, UploadFileForm

menu = [
    {'title': "Добавить десерт", 'url_name': 'add_dessert'},
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'}
]

cats_db = [
 {'id': 1, 'name': 'Пирожные'},
 {'id': 2, 'name': 'Торты'},
 {'id': 3, 'name': 'Печенье'},
]


class CaralogIndex(ListView):
    template_name = 'catalog/index.html'
    context_object_name = 'cakes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['menu'] = menu
        context['cat_selected'] = 0
        return context
    
    def get_queryset(self):
        return Dessert.stocked.all().select_related('category')


class DessertCategory(ListView):
    template_name = 'catalog/index.html'
    context_object_name = 'cakes'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context['cakes'][0].category
        context['title'] = category.name
        context['menu'] = menu
        context['cat_selected'] = category.id
        return context
    
    def get_queryset(self):
        return Dessert.stocked.filter(
            category__slug=self.kwargs['category_slug']).select_related('category')


class TagDessertList(ListView):
    template_name = 'catalog/index.html'
    context_object_name = 'cakes'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagDessert.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = 'Тег: ' + tag.tag
        context['menu'] = menu
        context['cat_selected'] = None
        return context
    
    def get_queryset(self):
        return Dessert.stocked.filter(
            tags__slug=self.kwargs['tag_slug']).select_related('category')


class ShowCake(DetailView):
    model = Dessert
    template_name = 'catalog/cake.html'
    slug_url_kwarg = 'cake_slug'
    context_object_name = 'cake'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['cake']
        context['menu'] = menu
        return context
    
    def get_object(self, queryset=None):
        return get_object_or_404(Dessert.stocked,
                                 slug=self.kwargs[self.slug_url_kwarg])


class AddDessert(CreateView):
        # form_class = AddDessertForm
        model = Dessert
        template_name = 'catalog/add_dessert.html'
        success_url = reverse_lazy('index')
        fields = '__all__'
        extra_context = { 'menu': menu, 'title': 'Добавление десерта', }


class UpdateDessert(UpdateView):
        model = Dessert
        template_name = 'catalog/add_dessert.html'
        success_url = reverse_lazy('index')
        fields = ['title', 'content', 'in_stock', 'image', 'price', 'category']
        extra_context = { 'menu': menu, 'title': 'Редактирование десерта', }

class DeleteDessert(DeleteView):
    model = Dessert
    template_name = 'catalog/delete_dessert.html'
    success_url = reverse_lazy('index')
    extra_context = { 'menu': menu, 'title': 'Удаление десерта', }

def handle_uploaded_file(f):
    name = f.name
    ext = ''
    if '.' in name:
        ext = name[name.rindex('.'):]
        name = name[:name.rindex('.')]
    suffix = str(uuid.uuid4())
    with open(f"uploads/{name}_{suffix}{ext}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(form.cleaned_data['file'])
    else:
        form = UploadFileForm()
    return render(request, 'catalog/about.html', {'title': 'О сайте',
                                                  'menu': menu, 'form': form})

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")


def dessert_detail(request, name):
    if name == 'eclair':
        url_redirect = reverse('index')
        return HttpResponseRedirect(url_redirect)
    return HttpResponse(f"<h1>Десерт {name} <h1>")

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
