from django.core.mail import send_mail
from moneyControl.celery import app
from django.conf import settings


@app.task
def send_email_task(subject, body, to):
    print(send_mail(subject, body, settings.EMAIL_HOST_USER, [to], fail_silently=False))
