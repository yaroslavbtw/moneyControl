from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import UserPreference
from django.contrib import messages
import os
import json


@login_required()
def preferences(request):
    user_preferences = UserPreference.objects.get(user=request.user)

    currency_data = []
    with open(os.path.join(settings.BASE_DIR, 'currencies.json'), 'r') as file:
        data = json.load(file)
        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})

    if request.method == 'GET':
        return render(request, template_name='userpreferences/base_preferences.html',
                      context={'user': request.user, 'currency_data': currency_data,
                               'current_currency': user_preferences.currency})
    else:
        currency = request.POST['currency']
        user_preferences.currency = currency
        user_preferences.save()
        messages.success(request, "Changes saved")
        return render(request, template_name='userpreferences/base_preferences.html',
                      context={'user': request.user, 'currency_data': currency_data,
                               'current_currency': user_preferences.currency})
