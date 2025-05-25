from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from .models import Dessert, Category, TagDessert, Comment
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
import uuid
from django.db import models
from django.core.paginator import Paginator
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .forms import AddDessertForm, UploadFileForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import DataMixin


menu = [
    {'title': "Добавить десерт", 'url_name': 'add_dessert'},
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'}
]

class CaralogIndex(DataMixin, ListView):
    template_name = 'catalog/index.html'
    context_object_name = 'cakes'

    def get_context_data(self, *, object_list=None, **kwargs):
        return self.get_mixin_context(super().get_context_data(**kwargs),
                                      title='', cat_selected=0)
    
    def get_queryset(self):
        return Dessert.stocked.all().select_related('category')


class DessertCategory(DataMixin, ListView):
    template_name = 'catalog/index.html'
    context_object_name = 'cakes'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context['cakes'][0].category
        return self.get_mixin_context(super().get_context_data(**kwargs),
                                      title=category.name,
                                      cat_selected=category.id)
    
    def get_queryset(self):
        return Dessert.stocked.filter(
            category__slug=self.kwargs['category_slug']).select_related('category')


class TagDessertList(DataMixin, ListView):
    template_name = 'catalog/index.html'
    context_object_name = 'cakes'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagDessert.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)
    
    def get_queryset(self):
        return Dessert.stocked.filter(
            tags__slug=self.kwargs['tag_slug']).select_related('category')


class ShowCake(DataMixin, DetailView):
    model = Dessert
    template_name = 'catalog/cake.html'
    slug_url_kwarg = 'cake_slug'
    context_object_name = 'cake'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['comment_form'] = CommentForm()
        return self.get_mixin_context(context, title=context['cake'])
    
    def get_object(self, queryset=None):
        return get_object_or_404(Dessert.stocked,
                                 slug=self.kwargs[self.slug_url_kwarg])


class AddDessert(DataMixin, CreateView):
        # form_class = AddDessertForm
    model = Dessert
    template_name = 'catalog/add_dessert.html'
    success_url = reverse_lazy('index')
    fields = '__all__'
    title_cake = 'Добавление десерта'

class AddComment(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    template_name = 'catalog/cake.html'
    login_url = reverse_lazy('users:login')
    
    def get_success_url(self):
        return reverse('cake', kwargs={'cake_slug': self.kwargs['cake_slug']})
    
    def form_valid(self, form):
        d = form.save(commit=False)
        d.author = self.request.user
        form.instance.dessert = get_object_or_404(Dessert.stocked, slug=self.kwargs['cake_slug'])
        return super().form_valid(form)
    
    def get(self, request, *args, **kwargs):
        return redirect('cake', cake_slug=self.kwargs['cake_slug'])


class UpdateDessert(UpdateView):
    model = Dessert
    template_name = 'catalog/add_dessert.html'
    success_url = reverse_lazy('index')
    fields = ['title', 'content', 'in_stock', 'image', 'price', 'category']
    title_cake = 'Редактирование десерта'

class DeleteDessert(DeleteView):
    model = Dessert
    template_name = 'catalog/delete_dessert.html'
    success_url = reverse_lazy('index')
    title_cake = 'Удаление десерта'

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

@login_required
def about(request):
    contact_list = Dessert.stocked.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'catalog/about.html', {'page_obj': page_obj,
                                                  'title': 'О сайте',
                                                  'menu': menu})

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
