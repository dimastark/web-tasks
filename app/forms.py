""" Формы для POST методов """
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms import CharField, TextInput, PasswordInput, Form, Textarea, forms


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


class RegistrationForm(Form):
    """ Форма регистрации """
    username = CharField(
        max_length=20,
        widget=TextInput({
            'class': 'form-control',
            'placeholder': 'Логин',
        })
    )
    password1 = CharField(
        label="Password",
        widget=PasswordInput({
            'class': 'form-control',
            'placeholder': 'Пасворд1',
        })
    )
    password2 = CharField(
        label="Repeat",
        widget=PasswordInput({
            'class': 'form-control',
            'placeholder': 'Пасворд2',
        })
    )

    def clean(self) -> dict:
        data = super(RegistrationForm, self).clean()
        first = data.get('password1')
        second = data.get('password2')
        if first != second:
            raise forms.ValidationError('Пароли не совпадают')
        try:
            User.objects.get(username__iexact=data['username'])
        except User.DoesNotExist:
            return data
        else:
            raise forms.ValidationError('Пользователь уже существует')


class CommentForm(Form):
    """ Комментарий """
    message = CharField(
        max_length=1000,
        widget=Textarea(attrs={
            'id': 'message',
            'placeholder': 'Бла бла бла...',
            'class': 'form-control',
            'rows': "7",
        })
    )
