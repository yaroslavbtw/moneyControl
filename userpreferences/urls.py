from django.urls import path
from .views import *

urlpatterns = [
    path('', preferences, name='preferences'),
]
