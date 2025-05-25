from django import forms
from .models import Category, Dessert, TagDessert, Comment
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.core.validators import MinLengthValidator, MaxLengthValidator


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = ("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжз"
    "ийклмнопрстуфхцчшщбыъэюя0123456789- ")
    code = 'russian'
    def __init__(self, message=None):
        self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."
    def __call__(self, value):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code, params={"value": value})


# class AddDessertForm(forms.Form):
#     title = forms.CharField(max_length=255, min_length=5, label="Название",
#                             widget=forms.TextInput(
#                                 attrs={'class': 'form-input'}),
#                             validators=[ RussianValidator(),],
#                             error_messages={'min_length':
#                                             'Слишком короткое название',
#                                             'required':
#                                             'Название - обязательное поле'})
#     slug = forms.SlugField(max_length=255, label="URL", validators=[
#         MinLengthValidator(5, message="Минимум 5 символов"),
#         MaxLengthValidator(100, message="Максимум 100 символов"),])
#     content = forms.CharField(widget=forms.Textarea(
#         attrs={'cols': 50, 'rows': 5}), required=False,
#                               label="Описание")
#     in_stock = forms.BooleanField(required=False, label="В наличии",
#                                   initial=True)
#     category = forms.ModelChoiceField(queryset=Category.objects.all(),
#                                       label="Категория",
#                                       empty_label="Категория не выбрана")
#     price = forms.IntegerField(min_value=50, label="Цена", error_messages={
#         'min_value': 'Слишком низкая цена',
#         'required': 'Цена - обязательное поле'})


class AddDessertForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      empty_label="Категория не выбрана",
                                      label="Категория")
    class Meta:
        model = Dessert
        fields = ['title', 'slug', 'content', 'in_stock', 'category',
                  'tags', 'price', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}), 
            'tags': forms.CheckboxSelectMultiple, }
        
    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise ValidationError('Цена не может быть отрицательной.')
        return price


class UploadFileForm(forms.Form):
    file = forms.FileField(label="Файл")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Введите ваш комментарий...'})
        }
