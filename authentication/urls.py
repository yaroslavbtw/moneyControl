from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt, csrf_protect

urlpatterns = [
    path('register/', csrf_protect(RegistrationView.as_view()), name='register'),
    path('login/', csrf_protect(LoginView.as_view()), name='login'),
    path('validate-username/', csrf_exempt(UsernameValidationView.as_view()), name='validateUsername'),
    path('validate-email/', csrf_exempt(EmailValidationView.as_view()), name='validateEmail'),
    path('reset-password/', csrf_protect(ResetPasswordView.as_view()), name='resetPassword'),
]
