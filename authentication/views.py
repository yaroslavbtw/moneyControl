from django.shortcuts import render
from django.views import View
import json
import re
from validate_email import validate_email
from django.http import JsonResponse
from django.contrib.auth.models import User
# Create your views here.


class UsernameValidationView(View):
    def post(self, request):
        username = json.loads(request.body)['username']
        if len(str(username)) < 5 or not str(username).isalnum():
            return JsonResponse(
                {'username_error': 'Your username must be 5-20 characters long, only contain letters and numbers.'})
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'This username is already in use.'})
        return JsonResponse({'username_valid': True})


class EmailValidationView(View):
    def post(self, request):
        email = json.loads(request.body)['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Your mail should look like a template: name@example.com.'})
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'This email is already in use.'})
        return JsonResponse({'email_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, template_name='authentication/register.html')


class LoginView(View):
    def get(self, request):
        return render(request, template_name='authentication/login.html')


class ResetPasswordView(View):
    def get(self, request):
        return render(request, template_name='authentication/reset-password.html')
