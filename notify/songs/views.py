from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.db.models import Q
import qrcode

from .forms import *
from .models import *
from .mixins import *


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    '''
    Добавить пост
    '''
    form_class = AddPostForm
    template_name = 'songs/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title='Post adding')
        return dict(list(context.items()) + list(g_def.items()))


class AddAuthor(LoginRequiredMixin, DataMixin, CreateView):
    '''
    Добавить автора
    '''
    form_class = AddAuthorForm
    template_name = 'songs/addauthor.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title='Performer adding')
        return dict(list(context.items()) + list(g_def.items()))


class AddAlbum(LoginRequiredMixin, DataMixin, CreateView):
    '''
    Добавить альбом
    '''
    form_class = AddAlbumForm
    template_name = 'songs/addalbum.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title='Album adding')
        return dict(list(context.items()) + list(g_def.items()))


class ShowAlbum(LoginRequiredMixin, DataMixin, DetailView):
    '''
    Просмотр одного альбома
    '''
    model = Album
    template_name = 'songs/showalbum.html'
    slug_url_kwarg = 'album_slug'
    context_object_name = 'album'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title=context['album'])
        return dict(list(context.items()) + list(g_def.items()))


class ShowPost(LoginRequiredMixin, DataMixin, DetailView):
    '''
    Просмотр одного поста
    '''
    model = Songs
    template_name = 'songs/showsong.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(g_def.items()))


class ShowAuthor(LoginRequiredMixin, DataMixin, DetailView):
    '''
    Просмотр одного исполнителя
    '''
    model = Author
    template_name = 'songs/showauthor.html'
    slug_url_kwarg = 'author_slug'
    context_object_name = 'author'

    def get_queryset(self):
        return Author.objects.filter(slug=self.kwargs['author_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g = Author.objects.get(slug=self.kwargs['author_slug'])
        g_def = self.get_user_context(title='Performer - ' + str(g.name),
                                      author_selected=g.pk)
        return dict(list(context.items()) + list(g_def.items()))


class Home(LoginRequiredMixin, DataMixin, ListView):
    '''
    Главная
    '''
    model = Songs
    template_name = 'songs/home_page.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title='Notify', genre_selected=0)
        return dict(list(context.items()) + list(g_def.items()))

    def get_queryset(self):
        return Songs.objects.filter(is_published=True)


class AuthorsList(LoginRequiredMixin, DataMixin, ListView):
    '''
    Страница испонителей
    '''
    model = Author
    template_name = 'songs/authors.html'
    context_object_name = 'authors'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title='Performers', author_selected=0)
        return dict(list(context.items()) + list(g_def.items()))

    def get_queryset(self):
        return Author.objects.all()


class RegisterUser(DataMixin, CreateView):
    '''
    Страница регистрации
    '''
    form_class = RegisterUserForm
    template_name = 'songs/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title='Sign up')
        return dict(list(context.items()) + list(g_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    '''
    Страница авторизации
    '''
    form_class = LoginUserForm
    template_name = 'songs/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title='Sign in')
        return dict(list(context.items()) + list(g_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


class ContactView(LoginRequiredMixin, DataMixin, FormView):
    '''
    Страница контакта
    '''
    form_class = ContactForm
    template_name = 'songs/contacus.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title='Contact')
        return dict(list(context.items()) + list(g_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


class AboutView(LoginRequiredMixin, DataMixin, TemplateView):
    '''
    Страница про нас
    '''
    template_name = 'songs/about.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title='About')
        return dict(list(context.items()) + list(g_def.items()))


class SearchView(DataMixin, LoginRequiredMixin, ListView):
    '''
    Страница найденых песен
    '''
    model = Songs
    template_name = 'songs/search_results.html'
    context_object_name = 'results'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title='Search')
        return dict(list(context.items()) + list(g_def.items()))

    def get_queryset(self):
        query = self.request.GET.get('q')
        results = []
        songs = Songs.objects.filter(Q(title__icontains=query))
        albums = Album.objects.filter(Q(name__icontains=query))
        authors = Author.objects.filter(Q(name__icontains=query))
        results += songs
        results += albums
        results += authors
        return results


def qr_code_page(request):
    '''
    Страница с QR-code
    '''
    return render(request, 'songs/qr.html')


def search_page(request):
    '''
    Страница поиска
    '''
    return render(request, 'songs/search.html')


def logout_user(request):
    '''
    Функция для выхода
    '''
    logout(request)
    return redirect('login')


def CustomErrorPage(request, exception):
    return render(request, 'songs/errorpage.html')


def generate_qr_code(request):
    '''
    Функция генерации QR-code
    '''
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data('https://github.com/CapitainFan/music_life')
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response
