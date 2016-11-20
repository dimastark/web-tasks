""" Definition of views. """

from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime
from app.utils import create_image


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
    return render(request, 'contact.html', {
            'name': 'contact',
            'title': 'Где я? Как я?',
            'message': 'Как меня найти?',
            'year': datetime.now().year,
        }
    )


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
        'me.png', 'antigravity.png', 'dont.png',
        'brainbreak.png', 'cat.png', 'todo.png',
        'compiling.png', 'catwizz.png', 'catwar.png',
        'gods.png', 'duck.png', 'python.png',
        'dont.png', 'team.png'
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
                create_image('wall1.png', 'wall1'),
                create_image('wall3.png', 'wall3'),
                create_image('wall4.png', 'wall4'),
            ]
        }
    )
