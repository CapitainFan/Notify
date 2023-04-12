from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .mixins import *


class Home(LoginRequiredMixin, ListView):
    model = Songs
    template_name = 'songs/main.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notify'
        return context


class Songss(LoginRequiredMixin, DataMixin, ListView):
    model = Songs
    template_name = 'songs/songs.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title='Songs', genre_selected=0)
        return dict(list(context.items()) + list(g_def.items()))

    def get_queryset(self):
        return Songs.objects.filter(is_published=True)


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
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
    model = Album
    template_name = 'songs/showalbum.html'
    slug_url_kwarg = 'album_slug'
    context_object_name = 'album'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title=context['album'])
        return dict(list(context.items()) + list(g_def.items()))


class ShowPost(LoginRequiredMixin, DataMixin, DetailView):
    model = Songs
    template_name = 'songs/showsong.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(g_def.items()))


class ShowAuthor(LoginRequiredMixin, DataMixin, DetailView):
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


class SongsGener(LoginRequiredMixin, DataMixin, ListView):
    model = Songs
    template_name = 'songs/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Songs.objects.filter(genre__slug=self.kwargs['genre_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g = Genre.objects.get(slug=self.kwargs['genre_slug'])
        g_def = self.get_user_context(title='Genre - ' + str(g.name),
                                      genre_selected=g.pk)
        return dict(list(context.items()) + list(g_def.items()))


class AuthorsList(LoginRequiredMixin, DataMixin, ListView):
    model = Author
    template_name = 'songs/authors.html'
    context_object_name = 'authors'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title='Performers', author_selected=0)
        return dict(list(context.items()) + list(g_def.items()))

    def get_queryset(self):
        return Author.objects.all()


class AlbumsList(LoginRequiredMixin, DataMixin, ListView):
    model = Album
    template_name = 'songs/albums.html'
    context_object_name = 'albums'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title='Albums', album_selected=0)
        return dict(list(context.items()) + list(g_def.items()))

    def get_queryset(self):
        return Album.objects.all()


class RegisterUser(DataMixin, CreateView):
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
    form_class = LoginUserForm
    template_name = 'songs/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title='Sign in')
        return dict(list(context.items()) + list(g_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


class ContactFormView(LoginRequiredMixin, DataMixin, FormView):
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
    template_name = 'songs/about.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title='About')
        return dict(list(context.items()) + list(g_def.items()))


def logout_user(request):
    logout(request)
    return redirect('login')


def pageNotFound(request, exception):
    return render(request, 'songs/pagenotfound.html')
