from django import forms
from .models import Category


class AddDessertForm(forms.Form):
    title = forms.CharField(max_length=255, label="Название")
    slug = forms.SlugField(max_length=255, label="URL")
    content = forms.CharField(widget=forms.Textarea(), required=False,
                              label="Описание")
    in_stock = forms.BooleanField(required=False, label="В наличии")
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      label="Категория")
    price = forms.IntegerField(min_value=0, label="Цена")
