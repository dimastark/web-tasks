""" Модели """
from datetime import datetime, date
from collections import namedtuple
from typing import List

from django.db.models import Model, CharField, BooleanField, DateTimeField, TextField
from django.http import HttpRequest

from app.forms import CommentForm
from app.utils import dict2namedtuple, get_client_ip, get_next_order


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
        all_visits = Visit.objects.all().order_by('-created').values()
        return [dict2namedtuple(dct) for dct in all_visits]

    @staticmethod
    def all_visits_count() -> int:
        return Visit.objects.filter(is_view=True).count()

    @staticmethod
    def today_visits_count() -> int:
        return Visit.objects.filter(
            is_view=True, created__gt=date.today()
        ).count()

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


class Comment(Model):
    username = CharField(max_length=20)
    message = TextField(max_length=1000)
    order = TextField(max_length=100)
    created = DateTimeField(auto_now_add=True)

    @staticmethod
    def make(request: HttpRequest, form: CommentForm):
        message = form.cleaned_data['message']
        username = request.user.get_username() or 'anonymous'
        order = get_next_order(request.POST['order'])
        new_comment = Comment(
            username=username,
            message=message,
            order=order
        )
        new_comment.save()
        created = new_comment.created
        return dict(
            created=created.strftime("%d %B %Y г. %H:%M").lstrip('0'),
            username=username,
            message=message,
            order=order,
            next=Comment.get_response_order(order)
        )

    @staticmethod
    def last_order():
        try:
            last = Comment.objects.all().order_by('-order')[0].order
            return last.split('_')[0]
        except IndexError:
            return '00000'

    @staticmethod
    def comment_tuples() -> List[namedtuple]:
        return [
            dict2namedtuple(dct)
            for dct in Comment.objects.all().order_by('order').values()
        ]

    @staticmethod
    def get_last_in_dialog(dialog):
        try:
            return Comment.objects.filter(
                order__startswith=dialog
            ).order_by('order')[1].order[:len(dialog) + 6]
        except IndexError:
            return None

    @staticmethod
    def get_response_order(dialog):
        last = Comment.get_last_in_dialog(dialog)
        last = get_next_order(last) if last else last
        return last or dialog + '_00000'

    @staticmethod
    def next_tuples():
        return [
            Comment.get_response_order(dct['order'])
            for dct in Comment.objects.all().order_by('order').values()
        ]

    @staticmethod
    def get_new_created(last_update):
        result = []
        for i in Comment.objects.filter(created__gt=last_update).values():
            dct = dict(i)
            dct.update({'next': get_next_order(i['order'])})
            result.append(dct)
        return result
