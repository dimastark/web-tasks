import locale
import os
import smtplib
from email.mime.text import MIMEText
from collections import namedtuple
from io import BytesIO

import datetime

from PIL import Image
from PIL import ImageDraw, ImageFont
from django.http import HttpRequest
from app.models import Visit

ImageModel = namedtuple('Image', ['src', 'thumb', 'id'])
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BASE_PATH = os.path.dirname(__file__)
FONT_PATH = os.path.join(BASE_PATH, 'static', 'app', 'fonts', 'Hack-Bold.ttf')


def dict2namedtuple(dictionary):
    return namedtuple('GenericDict', dictionary.keys())(**dictionary)


def get_last_visit(page, user_ip):
    try:
        return Visit.objects.filter(ip=user_ip, page=page).order_by('-id')[1].created
    except IndexError:
        return datetime.datetime.now()


def get_visits_count():
    now_day = datetime.date.today()
    all_views = Visit.objects.filter(is_view=True).count()
    today_views = Visit.objects.filter(is_view=True, created__gt=now_day).count()
    return all_views, today_views


def get_views_count():
    now_day = datetime.date.today()
    all_views = Visit.objects.count()
    today_views = Visit.objects.filter(created__gt=now_day).count()
    return all_views, today_views


def get_counter_lines(page, ip):
    all_views, today_views = get_views_count()
    all_visits, today_visits = get_visits_count()
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    return [
        'ПРОСМОТРОВ:     ПОСЕЩЕНИЙ:',
        'Всего:   {:<6} Всего:   {}'.format(all_views, all_visits),
        'Сегодня: {:<6} Сегодня: {}'.format(today_views, today_visits),
        '', 'Последнее посещение этой',
        get_last_visit(page, ip).strftime("%A, %d.%m.%Y %H:%M")
    ]


def get_counter_image(page, ip):
    lines = get_counter_lines(page, ip)
    img = Image.new("RGBA", (240, 100), WHITE)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, 12)
    for i, line in enumerate(lines):
        draw.text((0, i * 15), line, BLACK, font=font)
    buf = BytesIO()
    img.save(buf, 'PNG')
    img.close()
    del draw
    buf.seek(0)
    return buf


def create_image(name, image_id):
    return ImageModel(
        'app/gallery/' + name + '.png',
        'app/gallery/' + name + '_tn.jpg',
        'image' + str(image_id)
    )


def send_me_message(message, sender, name):
    msg = MIMEText(message, 'plain', 'utf-8')
    me = 'dstarkdev@gmail.com'
    bot = 'odlyamenya@mail.ru'
    msg['Subject'] = 'Сообщение от: "{}" с email: {}'.format(name, sender)
    msg['From'] = bot
    msg['To'] = me
    mail_server = smtplib.SMTP('smtp.mail.ru', 587)
    mail_server.ehlo()
    mail_server.starttls()
    mail_server.ehlo()
    mail_server.login(bot, 'Abcd1234')
    mail_server.sendmail(bot, me, msg.as_string())
    mail_server.quit()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def make_visit(request: HttpRequest, page):
    visited = request.session.get('visited', False)
    Visit.objects.create(
        ip=get_client_ip(request),
        page=page,
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        resolution='',
        method=request.method,
        is_view=not visited,
        browser_family=request.user_agent.browser.family,
        browser_version=request.user_agent.browser.version_string,
        device=request.user_agent.device.family,
        os=request.user_agent.os.family
    )
    request.session['visited'] = True


def get_visit_tuples():
    return [
        dict2namedtuple(dct) for dct in
        Visit.objects.all().order_by('-created').values()
    ]
