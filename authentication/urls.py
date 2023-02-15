from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt, csrf_protect

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('activate/<uuid64>/<token>/', VerificationView.as_view(), name='activate'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('validate-username/', csrf_exempt(UsernameValidationView.as_view()), name='validateUsername'),
    path('validate-email/', csrf_exempt(EmailValidationView.as_view()), name='validateEmail'),
    path('reset-password/get-link/', RequestResetPasswordView.as_view(), name='resetPasswordGetLink'),
    path('reset-password/new-password/<uuid64>/<token>/', ResetPasswordView.as_view(), name='resetPasswordNewPassword')
]
