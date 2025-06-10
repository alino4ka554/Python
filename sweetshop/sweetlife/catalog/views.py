from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound,  JsonResponse
from .models import Dessert, Category, TagDessert, Comment, Feedback, Like
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
import uuid
from django.db import models
from django.core.paginator import Paginator
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView
from .forms import AddDessertForm, UploadFileForm, CommentForm, FeedbackForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import DataMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.conf import settings


menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Обратная связь", 'url_name': 'contact'},
]

class CatalogIndex(DataMixin, ListView):
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
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        return self.get_mixin_context(context, title=context['cake'])
    
    def get_object(self, queryset=None):
        return get_object_or_404(Dessert.stocked,
                                 slug=self.kwargs[self.slug_url_kwarg])


class AddDessert(PermissionRequiredMixin, DataMixin, CreateView):
        # form_class = AddDessertForm
    model = Dessert
    template_name = 'catalog/add_dessert.html'
    success_url = reverse_lazy('index')
    fields = '__all__'
    title_cake = 'Добавление десерта'
    permission_required = 'catalog.add_dessert'

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


class UpdateDessert(PermissionRequiredMixin, UpdateView):
    model = Dessert
    template_name = 'catalog/add_dessert.html'
    success_url = reverse_lazy('index')
    fields = ['title', 'content', 'in_stock', 'image', 'price', 'category']
    title_cake = 'Редактирование десерта'
    permission_required = 'women.change_women'

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

class AboutView(DataMixin, TemplateView):
    template_name = 'catalog/about.html'


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

class LikeDessert(LoginRequiredMixin, View):
    def post(self, request, cake_slug):
        dessert = get_object_or_404(Dessert, slug=cake_slug)
        like, created = Like.objects.get_or_create(user=request.user, dessert=dessert)
        
        if not created:
            like.delete()
            return JsonResponse({'status': 'unliked', 'likes_count': dessert.likes.count()})
        
        return JsonResponse({'status': 'liked', 'likes_count': dessert.likes.count()})

class DeleteComment(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'catalog/cake.html'
    success_url = reverse_lazy('index')
    
    def get_success_url(self):
        return reverse('cake', kwargs={'cake_slug': self.object.dessert.slug})
    
    def get_object(self, queryset=None):
        comment = super().get_object(queryset)
        if comment.author != self.request.user and not self.request.user.has_perm('catalog.delete_comment'):
            raise PermissionDenied
        return comment

class FavoriteDesserts(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'catalog/favorites.html'
    context_object_name = 'cakes'
    title_cake = 'Избранное'

    def get_queryset(self):
        return Dessert.objects.filter(likes__user=self.request.user).select_related('category')
    
class ContactView(LoginRequiredMixin, DataMixin, CreateView):
    form_class = FeedbackForm
    template_name = 'catalog/contact.html'
    success_url = reverse_lazy('contact')
    title_cake = 'Обратная связь'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feedbacks'] = Feedback.objects.all().select_related('user')
        return context

class FeedbackListView(ListView):
    model = Feedback
    template_name = 'catalog/feedback_list.html'
    context_object_name = 'feedbacks'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Отзывы'
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        return context

class EditFeedbackView(LoginRequiredMixin, UpdateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'catalog/edit_feedback.html'
    success_url = reverse_lazy('feedback_list')

    def get_queryset(self):
        return Feedback.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать отзыв'
        return context
