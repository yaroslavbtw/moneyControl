from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('expenses/', include('expenses.urls')),
    path('incomes/', include('incomes.urls')),
    path('authentication/', include('authentication.urls')),
    path('preferences/', include('userpreferences.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
]
