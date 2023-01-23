from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('validate-username/', csrf_exempt(UsernameValidationView.as_view()), name='validateUsername'),
    path('reset-password/', csrf_exempt(ResetPasswordView.as_view()), name='resetPassword'),
]
