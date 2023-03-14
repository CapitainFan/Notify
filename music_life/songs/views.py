from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .mixins import *


class Home(DataMixin, ListView):
    model = Songs
    template_name = 'songs/index.html'
    context_object_name = 'songs'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(g_def.items()))

    def get_queryset(self):
        return Songs.objects.filter(is_published=True)


class AddSong(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddSongForm
    template_name = 'songs/addsong.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(g_def.items()))


class AddAuthor(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddSongForm
    template_name = 'songs/addauthor.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title="Добавление автора")
        return dict(list(context.items()) + list(g_def.items()))


class ShowSong(DataMixin, DetailView):
    model = Songs
    template_name = 'songs/showsong.html'
    slug_url_kwarg = 'song_slug'
    context_object_name = 'song'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title=context['song'])
        return dict(list(context.items()) + list(g_def.items()))


class ShowAuthor(DataMixin, DetailView):
    model = Author
    template_name = 'songs/showauthor.html'
    slug_url_kwarg = 'author_slug'
    context_object_name = 'author'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title=context['author'])
        return dict(list(context.items()) + list(g_def.items()))


class SongGener(DataMixin, ListView):
    model = Songs
    template_name = 'songs/index.html'
    context_object_name = 'gener'
    allow_empty = False

    def get_queryset(self):
        return Songs.objects.filter(gener__slug=self.kwargs['gener_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g = Genre.objects.get(slug=self.kwargs['gener_slug'])
        g_def = self.get_user_context(title='Жанр - ' + str(g.name),
                                      gener_selected=g.pk)
        return dict(list(context.items()) + list(g_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'songs/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title="Регистрация")
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
        g_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(g_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'songs/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(g_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


class AboutView(DataMixin, TemplateView):
    template_name = 'songs/about.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        g_def = self.get_user_context(title="О сайте")
        return dict(list(context.items()) + list(g_def.items()))


def logout_user(request):
    logout(request)
    return redirect('home')


def pageNotFound(request, exception):
    return render(request, 'songs/pagenotfound.html')
