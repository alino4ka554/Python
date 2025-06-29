from django.contrib import messages
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Dessert, Category

class IngredientsFilter(admin.SimpleListFilter):
    title = 'Наличие состава'
    parameter_name = 'ingredients'

    def lookups(self, request, model_admin):
        return [('yes', 'Имеется'), ('no', 'Отсутсвует'),]
    
    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(info__isnull=False)
        elif self.value() == 'no':
            return queryset.filter(info__isnull=True)


@admin.register(Dessert)
class DessertAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'slug', 'category', 'tags', 'image',
              'dessert_image']
    filter_horizontal = ['tags']
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'in_stock', 'category', 'tags_count',
                    'dessert_image')
    readonly_fields = ['dessert_image']
    list_display_links = ('title', )
    ordering = ['in_stock', 'title']
    list_editable = ('in_stock', )
    list_per_page = 5
    actions = ['set_instock', 'set_outofstack']
    search_fields = ['title', 'category__name']
    list_filter = [IngredientsFilter, 'category__name', 'in_stock']

    @admin.display(description="Изображение")
    def dessert_image(self, dessert: Dessert):
        if dessert.image:
            return mark_safe(f"<img src='{dessert.image.url}'width=50>")
        return "Без изображения"
    
    @admin.display(description="Количество тегов")
    def tags_count(self, dessert: Dessert):
        return f"{dessert.tags.count()}"
    
    @admin.action(description="Отобразить выбранные десерты в каталоге")
    def set_instock(self, request, queryset):
        count = queryset.update(in_stock=Dessert.Status.INSTOCK)
        self.message_user(request, f"Изменено {count} десерта(ов).")

    @admin.action(description="Убрать выбранные десерты из каталога")
    def set_outofstack(self, request, queryset):
        count = queryset.update(in_stock=Dessert.Status.OUTOFSTOCK)
        self.message_user(request, f"{count} десерта(ов) убраны из каталога!",
                          messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
