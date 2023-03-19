from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Добавить автора", 'url_name': 'add_author'},
        {'title': "Обратная связь", 'url_name': 'contact'},
]

class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        genres = Genre.objects.all()
        user_menu = menu.copy()

        if not self.request.user.is_authenticated:
            user_menu.pop(1)
            user_menu.pop(1)

        context['menu'] = user_menu
        context['genres'] = genres

        if 'genre_selected' not in context:
            context['genre_selected'] = 0

        return context
