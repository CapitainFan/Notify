from .models import *

class DataMixin:
    '''
    Базовый mixin для view классов
    '''
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        genres = Genre.objects.all()

        context['genres'] = genres

        if 'genre_selected' not in context:
            context['genre_selected'] = -1

        if 'author_selected' not in context:
            context['author_selected'] = -1

        if 'album_selected' not in context:
            context['album_selected'] = -1

        return context
