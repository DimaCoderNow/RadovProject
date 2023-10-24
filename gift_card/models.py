from django.db import models
from django.contrib.auth.models import User


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    number = models.CharField(max_length=16, unique=False)
    nominal = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'
        ordering = ['-modified']

