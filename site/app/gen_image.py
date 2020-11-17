import locale
import os
from io import BytesIO
from typing import List

from PIL import Image, ImageDraw, ImageFont

from app.models import Visit

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BASE_PATH = os.path.dirname(__file__)
FONT_PATH = os.path.join(BASE_PATH, 'static', 'app', 'fonts', 'Hack-Bold.ttf')


def get_counter_lines(page: str, ip: str) -> List[str]:
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    return [
        'ПРОСМОТРОВ:     ПОСЕЩЕНИЙ:',
        'Всего:   {:<6} Всего:   {}'.format(
            Visit.all_views_count(),
            Visit.all_visits_count(),
        ),
        'Сегодня: {:<6} Сегодня: {}'.format(
            Visit.today_views_count(),
            Visit.today_visits_count(),
        ),
        '', 'Последнее посещение этой',
        Visit.get_last_visit_of(page, ip).strftime("%A, %d.%m.%Y %H:%M"),
    ]


def get_counter_image(page: str, ip: str) -> BytesIO:
    lines = get_counter_lines(page, ip)
    image = Image.new('RGBA', (240, 100), WHITE)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_PATH, 12)
    for i, line in enumerate(lines):
        draw.text((0, i * 15), line, BLACK, font=font)
    buffer = BytesIO()
    image.save(buffer, 'PNG')
    image.close()
    del draw
    buffer.seek(0)
    return buffer
