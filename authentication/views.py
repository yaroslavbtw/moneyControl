from django.shortcuts import render, redirect, reverse
from django.views import View
import json
from validate_email import validate_email
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .utils import confirm_token_generator, reset_password_generator
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import update_session_auth_hash
from django.contrib import auth
from django.core.cache import cache
from .tasks import send_html_email_task


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
                messages.add_message(request, messages.SUCCESS, "Your account registered! "
                                                                "Check your email to confirm registration")

                domain = get_current_site(request).domain
                uuid64 = urlsafe_base64_encode(force_bytes(user.pk))
                link = reverse('activate', kwargs={'uuid64': uuid64, 'token': confirm_token_generator.make_token(user)})
                activate_url = 'http://' + domain + link

                html_content = render(request, 'partials/email_message.html',
                                      {'username': user.username, 'title': 'Confirm Registration', 'text_part1':
                                          'You have successfully registered on our website. '
                                          'We are very happy to welcome you to our community.',
                                       'text_part2': 'To complete your registration, please follow this link.',
                                       'link': activate_url}).content.decode('utf-8')

                send_html_email_task.delay(subject='Money Control | Confirm Registration', to_emails=[email],
                                           html_content=html_content)
                user.save()
                return redirect('login')
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
                return redirect('login' + '?message=Account already activated')

            user.is_active = True
            user.save()

            return redirect('login')

        except (DjangoUnicodeDecodeError, User.DoesNotExist) as e:
            messages.error(request, str(e))
            return redirect('login')


class LoginView(View):

    def get(self, request):
        return render(request, template_name='authentication/login.html')

    def post(self, request):
        username = request.POST['usernameField']
        password = request.POST['passwordField']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, f"Welcome, {user.username}. You are now logged in.")
                    return redirect('expenses')
                messages.error(request, "Account is not activated. Please, check your email.")
                return render(request, template_name='authentication/login.html')
            messages.error(request, "Username entered incorrectly or password does not match.")
            return render(request, template_name='authentication/login.html')
        messages.error(request, "Fill in all the fields.")
        return render(request, template_name='authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('login')


class RequestResetPasswordView(View):

    def get(self, request):
        return render(request, template_name='authentication/reset-password-link.html')

    def post(self, request):
        email = request.POST['emailField']

        if not validate_email(email):
            messages.error(request, 'Please supply a valid email')
            return render(request, template_name='authentication/reset-password-link.html')
        try:
            user = User.objects.filter(email=email)[0]
            user.is_active = False
            user.profile.reset_password = True
            user.save()

            messages.add_message(request, messages.SUCCESS, "A link to reset your password has been sent to your email")

            domain = get_current_site(request).domain

            uuid64 = urlsafe_base64_encode(force_bytes(user.pk))
            link = reverse('resetPasswordNewPassword', kwargs={'uuid64': uuid64,
                                                               'token': reset_password_generator.make_token(user)})
            reset_url = 'http://' + domain + link

            html_content = render(request, 'partials/email_message.html',
                                  {'username': user.username, 'title': 'Reset Password', 'text_part1':
                                      ' You have successfully reset password of your account.', 'text_part2':
                                      'To change your password, please follow this link.', 'link': reset_url})\
                .content.decode('utf-8')

            send_html_email_task.delay(subject='Money Control | Reset password', to_emails=[email],
                                       html_content=html_content)
        except User.DoesNotExist:
            messages.error(request, 'User with this email does not exist')
            return render(request, template_name='authentication/reset-password-link.html')

        return render(request, 'authentication/reset-password-link.html', context={'fieldValues': request.POST})


class ResetPasswordView(View):

    def get(self, request, uuid64, token):
        try:
            id = force_str(urlsafe_base64_decode(uuid64))
            user = User.objects.get(pk=id)

        except User.DoesNotExist as e:
            messages.error(request, str(e))
            user = None

        if user is not None and reset_password_generator.check_token(user, token):
            context = {
                'uuid64': uuid64,
                'token': token
            }
            return render(request, template_name='authentication/reset-password-setPassword.html', context=context)

        return redirect('login')

    def post(self, request, uuid64, token):
        try:
            id = force_str(urlsafe_base64_decode(uuid64))
            user = User.objects.get(pk=id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            messages.add_message(request, messages.WARNING, str(e))
            user = None

        if user is not None and reset_password_generator.check_token(user, token):

            password = request.POST['passwordField']
            repeatPassword = request.POST['repeatPasswordField']

            if password == repeatPassword:
                user.set_password(password)
                user.profile.reset_password = False
                user.is_active = True
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password reset successfully.')
                return redirect('login')
            else:
                messages.error(request, 'Passwords mismatch')
                context = {
                    'uuid64': uuid64,
                    'token': token
                }
                return render(request, template_name='authentication/reset-password-link.html', context=context)
        else:
            messages.error(request, 'Not valid password')
            return render(request, template_name='authentication/reset-password-link.html')

