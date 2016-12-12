""" Definition of views. """
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpRequest
from datetime import datetime

from app.forms import ContactForm, BootstrapAuthenticationForm, register_form
from app.utils import create_image, send_me_message


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(request, 'index.html', {
            'name': 'home',
            'title': 'Домашняя',
            'year': datetime.now().year,
        }
    )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            send_me_message(data['message'], data['your_email'], data['your_name'])
            return redirect('thanks/')
    return render(request, 'contact.html', {
            'name': 'contact',
            'form': ContactForm,
            'title': 'Где я? Как я?',
            'message': 'Как меня найти?',
            'year': datetime.now().year,
        }
    )


def register(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = register_form(request.POST)
        if form:
            name, password = form
            User.objects.create_user(
                username=name,
                password=password,
            )
            return redirect('thanks/')
        else:
            return render(request, 'login.html', {
                'form': BootstrapAuthenticationForm,
                'name': 'login',
                'title': 'Вход',
                'year': datetime.now().year,
                'error': 'Либо пароли не совпали, либо логин занят'
            })
    return render(request, 'login.html', {
        'form': BootstrapAuthenticationForm,
        'name': 'login',
        'title': 'Вход',
        'year': datetime.now().year,
        'error': None,
    })


def comments(request):
    """Renders the comments page."""
    assert isinstance(request, HttpRequest)
    return render(request, 'notfound.html', {
            'name': 'comments',
            'title': 'Комменты и отзывы',
            'message': '404',
            'additional': 'Тут можно будет писать гневные комментарии',
            'year': datetime.now().year,
        }
    )


def images(request):
    """Renders the images page."""
    assert isinstance(request, HttpRequest)
    images_lst = [
        'me', 'antigravity', 'dont',
        'brainbreak', 'cat', 'todo',
        'compiling', 'catwizz', 'catwar',
        'gods', 'duck', 'python',
        'dont', 'team'
    ]
    return render(request, 'gallery.html', {
            'name': 'images',
            'title': 'Картиночки',
            'year': datetime.now().year,
            'images': [
                create_image(image, i)
                for i, image in enumerate(images_lst)
            ],
            'wallpapers': [
                create_image('wall1', 'wall1'),
                create_image('wall3', 'wall3'),
                create_image('wall4', 'wall4'),
            ]
        }
    )


def thanks(request):
    """Renders the images page."""
    assert isinstance(request, HttpRequest)
    return render(request, 'thanks.html')
