""" Definition of models. """

from django.db import models


class Visit(models.Model):
    ip = models.CharField(max_length=15)
    page = models.CharField(max_length=10)
    user_agent = models.CharField(max_length=255)
    resolution = models.CharField(max_length=10)
    method = models.CharField(max_length=10)
    is_view = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
