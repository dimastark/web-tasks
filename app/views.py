""" Definition of views. """

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime


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


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(request, 'about.html', {
            'name': 'about',
            'title': 'ЧаВО',
            'message': 'Че это?',
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
    return render(request, 'notfound.html', {
            'name': 'images',
            'title': 'Картиночки',
            'message': '404',
            'additional': "Здесь скоро будут смешные мемасы и красивые изображения",
            'year': datetime.now().year,
        }
    )
