from django.urls import path

from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('logout/', logout_user, name='logout'),
    path('login/', LoginUser.as_view(), name='login'),
    path('about/', AboutView.as_view(), name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('addalbum/', AddAlbum.as_view(), name='add_album'),
    path('addauthor/', AddAuthor.as_view(), name='add_author'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('author/<slug:author_slug>/', ShowAuthor.as_view(), name='author'),
    path('genre/<slug:genre_slug>/', SongsGener.as_view(), name='genre'),
]
