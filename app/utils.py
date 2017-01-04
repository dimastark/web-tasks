import smtplib
from collections import namedtuple
from email.mime.text import MIMEText
from django.http import HttpRequest
from multiprocessing import Process

ImageModel = namedtuple('Image', ['src', 'thumb', 'id'])


def dict2namedtuple(d: dict) -> namedtuple:
    return namedtuple('GenericDict', d.keys())(**d)


def send_me_message(message: str, sender: str, name: str):
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


def send_mail_in_process(data: dict):
    proc = Process(
        target=send_me_message,
        args=(data['message'], data['your_email'], data['your_name'])
    )
    proc.daemon = True
    proc.start()


def get_client_ip(request: HttpRequest) -> str:
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def create_image(name: str, image_id: str) -> namedtuple:
    return ImageModel(
        'app/gallery/' + name + '.png',
        'app/gallery/' + name + '_tn.jpg',
        'image' + str(image_id)
    )


def get_next_order(order: str) -> str:
    parts = order.split('_')
    parts[-1] = '{0:05d}'.format(int(parts[-1]) + 1)
    return '_'.join(parts)
