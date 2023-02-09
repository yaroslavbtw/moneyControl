from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse


def settings(request):
    return render(request, template_name='userpreferences/base_preferences.html')
