from django import forms
from .models import Category
from django.core.validators import MinLengthValidator, MaxLengthValidator


class AddDessertForm(forms.Form):
    title = forms.CharField(max_length=255, min_length=5, label="Название",
                            widget=forms.TextInput(
                                attrs={'class': 'form-input'}),
                            error_messages={'min_length':
                                            'Слишком короткое название',
                                            'required':
                                            'Название - обязательное поле'})
    slug = forms.SlugField(max_length=255, label="URL", validators=[
        MinLengthValidator(5, message="Минимум 5 символов"),
        MaxLengthValidator(100, message="Максимум 100 символов"),])
    content = forms.CharField(widget=forms.Textarea(
        attrs={'cols': 50, 'rows': 5}), required=False,
                              label="Описание")
    in_stock = forms.BooleanField(required=False, label="В наличии",
                                  initial=True)
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      label="Категория",
                                      empty_label="Категория не выбрана")
    price = forms.IntegerField(min_value=50, label="Цена", error_messages={
        'min_value': 'Слишком низкая цена',
        'required': 'Цена - обязательное поле'})
