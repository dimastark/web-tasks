import smtplib
from email.mime.text import MIMEText
from collections import namedtuple


Image = namedtuple('Image', ['src', 'thumb', 'id'])


def create_image(name, image_id):
    return Image(
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
