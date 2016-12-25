""" Формы для POST методов """
from typing import Optional, Tuple

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms import CharField, TextInput, PasswordInput, Form, Textarea


class BootstrapAuthenticationForm(AuthenticationForm):
    """ Форма с бутстрапом """
    username = CharField(
        max_length=20,
        widget=TextInput({
            'class': 'form-control',
            'placeholder': 'Логин',
        })
    )
    password = CharField(
        label="Password",
        widget=PasswordInput({
            'class': 'form-control',
            'placeholder': 'Пасворд',
        })
    )


class ContactForm(Form):
    """ Форма обратной связи """
    your_name = CharField(
        max_length=20,
        widget=TextInput(attrs={
            'placeholder': 'Как звать?',
            'class': 'form-control',
        })
    )
    your_email = CharField(
        max_length=254,
        widget=TextInput(attrs={
            'placeholder': 'Какая почта?',
            'class': 'form-control',
            'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$',
        })
    )
    message = CharField(
        max_length=255,
        widget=Textarea(attrs={
            'id': 'message',
            'placeholder': 'Что вы хотите мне сказать?',
            'class': 'form-control',
            'rows': "7",
        })
    )


def register_from_request(post) -> Optional[Tuple[str, str]]:
    """ Зарегестрировать по {{ post }} запросу """
    if post['password1'] == post['password2']:
        try:
            User.objects.get(username__iexact=post['username'])
        except User.DoesNotExist:
            return post['username'], post['password1']
