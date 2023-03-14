from django.urls import path

from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('logout/', logout_user, name='logout'),
    path('login/', LoginUser.as_view(), name='login'),
    path('about/', AboutView.as_view(), name='about'),
    path('addsong/', AddSong.as_view(), name='add_song'),
    path('addauthor/', AddAuthor.as_view(), name='add_author'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('song/<slug:song_slug>/', ShowSong.as_view(), name='song'),
    path('genre/<slug:genre_slug>/', SongGener.as_view(), name='genre'),
    path('author/<slug:author_slug>/', SongGener.as_view(), name='author'),
]
