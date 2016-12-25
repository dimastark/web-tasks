""" Модели """
from datetime import datetime, date
from collections import namedtuple
from typing import List

from django.db.models import Model, CharField, BooleanField, DateTimeField
from django.http import HttpRequest

from app.utils import dict2namedtuple, get_client_ip


class Visit(Model):
    ip = CharField(max_length=15)
    os = CharField(max_length=50)
    page = CharField(max_length=10)
    device = CharField(max_length=50)
    method = CharField(max_length=10)
    resolution = CharField(max_length=10)
    is_view = BooleanField(default=False)
    user_agent = CharField(max_length=255)
    browser_family = CharField(max_length=100)
    browser_version = CharField(max_length=50)
    created = DateTimeField(auto_now_add=True)

    @staticmethod
    def visit_tuples() -> List[namedtuple]:
        return [
            dict2namedtuple(dct)
            for dct in Visit.objects.all().order_by('-created').values()
        ]

    @staticmethod
    def all_visits_count() -> int:
        return Visit.objects.filter(is_view=True).count()

    @staticmethod
    def today_visits_count() -> int:
        return Visit.objects.filter(is_view=True, created__gt=date.today()).count()

    @staticmethod
    def all_views_count() -> int:
        return Visit.objects.count()

    @staticmethod
    def today_views_count() -> int:
        return Visit.objects.filter(created__gt=date.today()).count()

    @staticmethod
    def get_last_visit_of(page: str, user_ip: str) -> datetime:
        try:
            return Visit.objects.filter(
                ip=user_ip, page=page
            ).order_by('-id')[1].created
        except IndexError:
            return datetime.now()

    @staticmethod
    def make(request: HttpRequest, page: str):
        visited = request.session.get('visited', False)
        Visit.objects.create(
            ip=get_client_ip(request), page=page, method=request.method,
            resolution='', is_view=not visited, os=request.user_agent.os.family,
            browser_version=request.user_agent.browser.version_string,
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            browser_family=request.user_agent.browser.family,
            device=request.user_agent.device.family,
        )
        request.session['visited'] = True
