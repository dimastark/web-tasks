""" Definition of urls for project. """
from datetime import datetime

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout

from app.forms import BootstrapAuthenticationForm
from app.views import home, comments, contact, images, register, visits, visits_list

admin.autodiscover()
urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^home$', home, name='home'),
    url(r'^contact$', contact, name='contact'),
    url(r'^comments$', comments, name='comments'),
    url(r'^list$', visits_list, name='visits'),
    url(r'^images$', images, name='images'),
    url(r'^visits$', visits, name='visits'),
    url(r'^login/$', login, {
        'template_name': 'login.html',
        'authentication_form': BootstrapAuthenticationForm,
        'extra_context': {
            'name': 'login',
            'title': 'Вход',
            'year': datetime.now().year,
        },
    }, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/', register, name='register'),
]
