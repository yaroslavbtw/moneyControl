from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserPreference(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(user) + 's' + 'preferences'


# @receiver(post_save, sender=User)
# def update_UserSettings(sender, instance, created, **kwargs):
#     if created:
#         UserSettings.objects.create(user=instance)
#     instance.UserSettings.save()
