class DessertSlugConverter:
    regex = "[A-Za-z-]+" 

    def to_python(self, value):
        """Преобразование из URL в Python-значение"""
        return value.lower().replace("-", " ")  

    def to_url(self, value):
        """Преобразование из Python-значения в URL"""
        return value.replace(" ", "-") 