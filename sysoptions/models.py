from django.db import models
from django.db.models import TextChoices


class DefaultKeys(TextChoices):
    """默认配置项"""
    swiper = 'swiper'


class SysOptions(models.Model):
    key = models.TextField(primary_key=True, unique=True, choices=DefaultKeys.choices)
    value = models.JSONField(default=dict, null=True)
