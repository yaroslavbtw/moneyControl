from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
# Create your views here.


class UsernameValidationView(View):
    def post(self, request):
        username = json.loads(request.body)['username']
        if len(str(username)) < 5:
            return JsonResponse({'username_error': 'username should be 5 characters minimal'})
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'})
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'username exists already'})
        return JsonResponse({'username_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, template_name='authentication/register.html')


class ResetPasswordView(View):
    def get(self, request):
        return render(request, template_name='authentication/reset-password.html')
