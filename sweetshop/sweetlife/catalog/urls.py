from django.contrib import admin
from django.urls import include, path, register_converter, reverse
from catalog import views, converters

register_converter(converters.DessertSlugConverter, 'dessert')

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<slug:category_slug>/', views.categories_by_slug, 
         name='category'),
    path('dessert/<dessert:name>/', views.dessert_detail, name='dessert_detail'),
    path('cake/<slug:cake_slug>/', views.cake_detail, name='cake'),
    path('tag/<slug:tag_slug>/', views.show_tag_dessert, name='tag'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('contact/', views.contact, name='contact'),
]
