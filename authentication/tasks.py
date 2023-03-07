from django.core.mail import send_mail
from moneyControl.celery import app
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


@app.task
def send_email_task(subject, body, to):
    send_mail(subject, body, settings.EMAIL_HOST_USER, [to], fail_silently=False)


@app.task
def send_html_email_task(subject, to_emails, html_content, text_content=None):
    email = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, to_emails)
    email.attach_alternative(html_content, "text/html")
    email.send()
