""" Все вьюхи """
from datetime import datetime

from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth.views import login, logout

from app.forms import BootstrapAuthenticationForm, RegistrationForm
from app.views import (
    home, images, comments, contact,
    visits, visits_list, register,
)

admin.autodiscover()
urlpatterns = [
    # Основные разделы сайта
    url(r'^home$', home, name='home'),
    url(r'^images$', images, name='images'),
    url(r'^comments$', comments, name='comments'),
    url(r'^contact$', contact, name='contact'),
    url(r'^$', home, name='home'),

    url(r'^list$', visits_list, name='visits'),
    url(r'^visits$', visits, name='visits'),

    # Разделы для работы с пользователями
    url(r'^register/', register, name='register'),
    url(r'^login/$', login, {
        'template_name': 'login.html',
        'authentication_form': BootstrapAuthenticationForm,
        'extra_context': {
            'name': 'login',
            'title': 'Вход',
            'registration_form': RegistrationForm,
            'year': datetime.now().year,
        }
    }, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),

    # Админка
    url(r'^admin/', include(admin.site.urls)),
]
