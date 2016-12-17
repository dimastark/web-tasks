import smtplib
from email.mime.text import MIMEText
from collections import namedtuple
from io import BytesIO

from PIL import Image
from PIL import ImageDraw
from django.http import HttpRequest
from app.models import Visit

ImageModel = namedtuple('Image', ['src', 'thumb', 'id'])


def get_counter_image(count):
    img = Image.new("RGBA", (290,320), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    buf = BytesIO()
    img.save(buf, 'PNG')
    img.close()
    buf.seek(0)
    return buf


def create_image(name, image_id):
    return ImageModel(
        'app/gallery/' + name + '.png',
        'app/gallery/' + name + '_tn.jpg',
        'image' + str(image_id)
    )


async def send_me_message(message, sender, name):
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
    Visit.objects.create(
        ip=get_client_ip(request),
        page=page,
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        resolution='',
        method=request.method
    )
