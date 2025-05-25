from catalog.utils import menu

def get_dessert_context(request):
    return {'menu': menu}