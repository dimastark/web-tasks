# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-03 14:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='message',
            field=models.TextField(max_length=1000),
        ),
    ]
