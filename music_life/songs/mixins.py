from .models import *

menu = [
    {'title': "Добавить автора", 'url_name': 'add_author'},
    {'title': "Добавить альбом", 'url_name': 'add_album'},
    {'title': "Добавить статью", 'url_name': 'add_page'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "О сайте", 'url_name': 'about'},
]

class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        genres = Genre.objects.all()
        user_menu = menu.copy()

        if not self.request.user.is_authenticated:
            for i in range(3):
                user_menu.pop(0)

        context['menu'] = user_menu
        context['genres'] = genres

        if 'genre_selected' not in context:
            context['genre_selected'] = 0

        return context
