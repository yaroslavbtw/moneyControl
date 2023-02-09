from django.shortcuts import render, redirect, reverse
from django.views import View
import json

from validate_email import validate_email
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .utils import confirm_token_generator

from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site


from django.contrib import auth
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

    def post(self, request):
        username = request.POST['usernameField']
        email = request.POST['emailField']
        password = request.POST['passwordField']
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                messages.add_message(request, messages.SUCCESS, "Your account registered!")

                domain = get_current_site(request).domain

                uuid64 = urlsafe_base64_encode(force_bytes(user.pk))
                link = reverse('activate', kwargs={'uuid64': uuid64, 'token': confirm_token_generator.make_token(user)})
                activate_url = 'http://' + domain + link

                send_mail('Django MoneyExpenses Registration',
                          f'Hello, {username}, please follow this link to complete your registration\n' + activate_url,
                          settings.EMAIL_HOST_USER,
                          [email])

                return HttpResponse("<h1>YOUR ACCOUNT REGISTERED!</h1>")
            else:
                messages.add_message(request, messages.ERROR, 'Account with this email registered already.')
        else:
            messages.add_message(request, messages.ERROR, 'Account with this username registered already.')
        return render(request, 'authentication/register.html', context={'fieldValues': request.POST})


class VerificationView(View):
    def get(self, request, uuid64, token):
        try:
            id = force_str(urlsafe_base64_decode(uuid64))
            user = User.objects.get(pk=id)

            if not confirm_token_generator.check_token(user, token):
                return redirect(reverse('login') + '?message=Account already activated')

            if user.is_active:
                return redirect(reverse('login'))
            user.is_active = True
            user.save()

            return redirect(reverse('login'))

        except Exception as ex:
            pass
        return redirect(reverse('login'))


class LoginView(View):
    def get(self, request):
        return render(request, template_name='authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, f"Welcome, {user.username}. You are now logged in.")
                    return render(request, template_name='expenses/index.html')
                messages.error(request, "Account is not activated. Please, check your email.")
                return render(request, template_name='authentication/login.html')
            messages.error(request, "Username entered incorrectly or password does not match.")
            return render(request, template_name='authentication/login.html')
        messages.error(request, "Fill in all the fields.")
        return render(request, template_name='authentication/login.html')


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        messages.success(request, "You have been logged out.")
        return redirect(reverse('login'))


class ResetPasswordView(View):
    def get(self, request):
        return render(request, template_name='authentication/reset-password.html')
