from django.contrib import admin
from django.urls import include, path, register_converter, reverse
from catalog import views, converters

register_converter(converters.DessertSlugConverter, 'dessert')

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/<int:category_id>/', views.categories, name='categories'),
    path('categories/<slug:category_slug>/', views.categories_by_slug, name='categories_by_slug'),
    path('dessert/<dessert:name>/', views.dessert_detail, name='dessert_detail')
]
