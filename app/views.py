""" Definition of views. """
from multiprocessing import Process
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpRequest
from datetime import datetime

from app.forms import ContactForm, BootstrapAuthenticationForm, register_from_request
from app.utils import create_image, send_me_message, make_visit, get_counter_image, get_client_ip, get_visit_tuples


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    make_visit(request, '/home')
    return render(request, 'index.html', {
            'name': 'home',
            'title': 'Домашняя',
            'year': datetime.now().year,
        }
    )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    make_visit(request, '/contact')
    btn_class = 'btn-primary'
    btn_text = 'Отправить'
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            proc = Process(
                target=send_me_message,
                args=(data['message'], data['your_email'], data['your_name'])
            )
            proc.daemon = True
            proc.start()
            btn_class = 'btn-success'
            btn_text = 'Спасибо!'
    return render(request, 'contact.html', {
        'name': 'contact',
        'button_class': btn_class,
        'button_text': btn_text,
        'form': ContactForm,
        'title': 'Где я? Как я?',
        'message': 'Как меня найти?',
        'year': datetime.now().year,
    })


def register(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    make_visit(request, '/register')
    if request.method == 'POST':
        form = register_from_request(request.POST)
        if form:
            name, password = form
            User.objects.create_user(
                username=name,
                password=password,
            )
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
    make_visit(request, '/comments')
    return render(request, 'notfound.html', {
            'name': 'comments',
            'title': 'Комменты и отзывы',
            'message': '404',
            'additional': 'Тут можно будет писать гневные комментарии',
            'year': datetime.now().year,
        }
    )


def visits_list(request):
    """Renders the comments page."""
    assert isinstance(request, HttpRequest)
    make_visit(request, '/list')
    tpls = get_visit_tuples()
    return render(request, 'visits.html', {
            'name': 'list',
            'title': 'Посещения',
            'visits': tpls,
            'year': datetime.now().year,
        }
    )


def images(request):
    """Renders the images page."""
    assert isinstance(request, HttpRequest)
    make_visit(request, '/images')
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


def visits(request):
    """Renders the images page."""
    assert isinstance(request, HttpRequest)
    make_visit(request, '/visits')
    bts = get_counter_image(request.GET.get('path'), get_client_ip(request)).read()
    response = HttpResponse(content=bts)
    response['Content-Type'] = 'image/png'
    response['Content-Disposition'] = 'attachment;filename=counter.png'
    return response
