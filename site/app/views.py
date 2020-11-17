""" Вьюхи """
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpRequest
from datetime import datetime

from app.forms import ContactForm, BootstrapAuthenticationForm, RegistrationForm, CommentForm
from app.models import Visit, Comment
from app.utils import get_client_ip, create_image, send_mail_in_process
from app.gen_image import get_counter_image


def home(request: HttpRequest):
    """ Домашняя """
    Visit.make(request, '/home')
    return render(request, 'index.html', {
        'name': 'home',
        'title': 'Домашняя',
        'year': datetime.now().year,
    })


def images(request: HttpRequest):
    """ Картиночки """
    Visit.make(request, '/images')
    images_list = [
        'me', 'antigravity', 'dont',
        'brainbreak', 'cat', 'todo',
        'compiling', 'catwizz', 'catwar',
        'gods', 'duck', 'python', 'team'
    ]
    return render(request, 'gallery.html', {
        'name': 'images',
        'title': 'Картиночки',
        'year': datetime.now().year,
        'images': [
            create_image(image, i)
            for i, image in enumerate(images_list)
        ],
        'wallpapers': [
            create_image('wall1', 'wall1'),
            create_image('wall3', 'wall3'),
            create_image('wall4', 'wall4'),
        ]
    })


def comments(request: HttpRequest):
    """ Отзывы """
    Visit.make(request, '/comments')
    if request.method == 'POST' and request.is_ajax():
        form = CommentForm(request.POST)
        if form.is_valid():
            response_data = Comment.make(request, form)
            return JsonResponse(response_data)
    return render(request, 'comments.html', {
        'name': 'comments',
        'title': 'Отзывы',
        'form': CommentForm,
        'last': Comment.last_order,
        'comments': list(zip(Comment.next_tuples(), Comment.comment_tuples())),
        'year': datetime.now().year,
    })


def comments_update(request: HttpRequest):
    """ Отзывы """
    Visit.make(request, '/comments/')
    if request.method == 'POST' and request.is_ajax():
        last_update = datetime.fromtimestamp(int(request.POST['last_update']) / 1e3)
        last = Comment.get_new_created(last_update)
        return JsonResponse({'comments': last})


def contact(request: HttpRequest):
    """ Связаться со мной """
    Visit.make(request, '/contact')
    btn_class, btn_text = 'btn-primary', 'Отправить'
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail_in_process(form.cleaned_data)
            btn_class, btn_text = 'btn-success', 'Спасибо!'
    return render(request, 'contact.html', {
        'name': 'contact',
        'button_class': btn_class,
        'button_text': btn_text,
        'form': ContactForm,
        'title': 'Где я? Как я?',
        'message': 'Как меня найти?',
        'year': datetime.now().year,
    })


def register(request: HttpRequest):
    """ Регистрация """
    Visit.make(request, '/register')
    error = None
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['nickname']
            password = form.cleaned_data['password1']
            User.objects.create_user(
                username=name,
                password=password,
            )
        else:
            error = form.errors['__all__'][0]
    return render(request, 'login.html', {
        'registration_form': RegistrationForm,
        'form': BootstrapAuthenticationForm,
        'name': 'login',
        'title': 'Вход',
        'year': datetime.now().year,
        'error': error
    })


def visits_list(request: HttpRequest):
    """ Список посещений """
    Visit.make(request, '/list')
    return render(request, 'visits.html', {
        'name': 'list',
        'title': 'Посещения',
        'visits': Visit.visit_tuples,
        'year': datetime.now().year,
    })


def visits(request: HttpRequest):
    """ Картинка про посещения """
    Visit.make(request, '/visits')
    response = HttpResponse(content=get_counter_image(
        request.GET.get('path'),
        get_client_ip(request),
    ).read())
    response['Content-Type'] = 'image/png'
    response['Content-Disposition'] = 'attachment;filename=counter.png'
    return response
