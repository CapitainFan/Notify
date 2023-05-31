from django.urls import include, path
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'albums', AlbumViewSet, basename='albums')
router.register(r'authors', AuthorViewSet, basename='authors')

urlpatterns = [
    path('', include(router.urls)),
    path('songs/', SongsApiList.as_view()),
    path('songs/update/<int:pk>/', SongsApiUpdate.as_view()),
    path('songs/destroy/<int:pk>/', SongsApiDestroy.as_view()),
]
