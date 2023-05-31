from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.models import MyUser
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from .models import *

from django.contrib.auth.forms import AuthenticationForm


class MyUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=254,
        required=True,
        label='Login',
        widget=forms.TextInput(attrs={'class': 'form-input'}),
    )
    email = forms.EmailField(
        required=True,
        max_length=254,
        help_text='Required. Enter a valid email address.',
        widget=forms.EmailInput(attrs={'class': 'form-input'}),
        label='Почта',
    )
    avatar = forms.ImageField(
        required=False,
        label='Аватарка',
    )
    first_name = forms.CharField(
        required=True,
        max_length=30,
        help_text='Required.',
        widget=forms.TextInput(attrs={'class': 'form-input'}),
    )
    last_name = forms.CharField(
        required=True,
        max_length=30, 
        help_text='Required.',
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
    )
    password2 = forms.CharField(
        label='Password again',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
    )

    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password1', 'password2', 'avatar', 'first_name', 'last_name')


class MyAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={'class': 'form-input'}),
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input'}),
    )


class AddPostForm(forms.ModelForm):
    '''
    Форма для добавления поста
    '''

    class Meta:
        model = Songs
        fields = ['title', 'slug', 'content', 'photo', 'author',
                  'genre', 'is_single','album', 'is_published',]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')

        return title


class AddAuthorForm(forms.ModelForm):
    '''
    Форма для добавления исполнителя
    '''
    class Meta:
        model = Author
        fields = ['name', 'slug', 'content', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }


class AddAlbumForm(forms.ModelForm):
    '''
    Форма для добавления альбома
    '''

    class Meta:
        model = Album
        fields = ['name', 'slug', 'author', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
        }


class ContactForm(forms.Form):
    '''
    Контакт форма с капчей
    '''
    name = forms.CharField(
        label='Имя',
        max_length=225,
    )
    last_name = forms.CharField(
        label='Фамилия',
        max_length=225,
    )
    email = forms.EmailField(
        label='Почта',
    )
    content = forms.CharField(
        label='Текст',
        max_length=225,
        widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}),
    )
    captcha = CaptchaField()
