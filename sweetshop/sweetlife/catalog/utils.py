menu = [
    {'title': "Добавить десерт", 'url_name': 'add_dessert'},
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'}
]


class DataMixin:
    title_cake = None
    extra_context = {}
    paginate_by = 4

    def __init__(self):
        if self.title_cake:
            self.extra_context['title'] = self.title_cake
        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = menu


    def get_mixin_context(self, context, **kwargs):
        if self.title_cake:
            context['title'] = self.title_cake
        context['menu'] = menu
        context['cat_selected'] = None
        context.update(kwargs)
        return context
