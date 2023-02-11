from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class UserPreference(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(UserPreference.user) + 's' + 'preferences'


@receiver(post_save, sender=User)
def create_userpreferences(sender, instance, created, **kwargs):
    if created:
        UserPreference.objects.create(user=instance)
