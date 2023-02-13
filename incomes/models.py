from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Incomes(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    source = models.CharField(max_length=255)

    def __str__(self):
        return self.description

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Incomes'


class Source(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Sources'

    def __str__(self):
        return self.name

