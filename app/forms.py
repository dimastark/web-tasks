""" Формы для POST методов """

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class BootstrapAuthenticationForm(AuthenticationForm):
    """ Форма с бутстрапом """
    username = forms.CharField(
        max_length=20,
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder': 'Логин',
        })
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput({
            'class': 'form-control',
            'placeholder': 'Пасворд',
        })
    )


class ContactForm(forms.Form):
    """ Форма обратной связи """
    your_name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': 'Как звать?',
            'class': 'form-control',
        })
    )
    your_email = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'placeholder': 'Какая почта?',
            'class': 'form-control',
            'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$',
        })
    )
    message = forms.CharField(
        max_length=255,
        widget=forms.Textarea(attrs={
            'id': 'message',
            'placeholder': 'Что вы хотите мне сказать?',
            'class': 'form-control',
            'rows': "7",
        })
    )


def register_from_request(post):
    """ Зарегестрировать по {{ post }} запросу """
    if post['password1'] == post['password2']:
        try:
            User.objects.get(username__iexact=post['username'])
        except User.DoesNotExist:
            return post['username'], post['password1']
