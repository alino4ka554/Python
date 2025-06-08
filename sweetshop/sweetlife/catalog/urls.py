from django.contrib import admin
from django.urls import include, path, register_converter, reverse
from catalog import views, converters

register_converter(converters.DessertSlugConverter, 'dessert')

urlpatterns = [
    path('', views.CaralogIndex.as_view(), name='index'),
    path('category/<slug:category_slug>/', views.DessertCategory.as_view(),
         name='category'),
    path('dessert/<dessert:name>/', views.dessert_detail, name='dessert_detail'),
    path('cake/<slug:cake_slug>/', views.ShowCake.as_view(), name='cake'),
    path('cake/<slug:cake_slug>/like/', views.LikeDessert.as_view(), name='like_dessert'),
    path('favorites/', views.FavoriteDesserts.as_view(), name='favorites'),
    path('tag/<slug:tag_slug>/', views.TagDessertList.as_view(), name='tag'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('contact/', views.contact, name='contact'),
    path('add_dessert/', views.AddDessert.as_view(), name='add_dessert'),
    path('edit/<slug:slug>/', views.UpdateDessert.as_view(), name='edit_dessert'),
    path('delete/<slug:slug>/', views.DeleteDessert.as_view(), name='delete_dessert'),
    path('cake/<slug:cake_slug>/comment/', views.AddComment.as_view(), name='add_comment'),
    path('comment/<int:pk>/delete/', views.DeleteComment.as_view(), name='delete_comment')
]
