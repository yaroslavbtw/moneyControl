from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Incomes, Source
from django.http import HttpResponseForbidden
from userpreferences.models import UserPreference
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q


@login_required()
def index(request):
    user_incomes = Incomes.objects.filter(owner=request.user)
    user_preferences = get_object_or_404(UserPreference, user=request.user)

    paginator = Paginator(user_incomes, 4)
    page_number = request.GET.get('page')
    if page_number:
        page_object = paginator.get_page(page_number)
    else:
        page_object = paginator.get_page(1)
    context = {
        'user': request.user,
        'currency': user_preferences.currency,
        'page_obj': page_object,
        'page_obj_length': len(page_object.object_list)
    }
    return render(request, template_name='incomes/index.html', context=context)


@login_required()
def add_incomes(request):
    source = Source.objects.all()
    context = {
        'user': request.user,
        'sources': source,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, template_name='incomes/add_incomes.html', context=context)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['date']
        if amount and description and source:
            if date:
                Incomes.objects.create(amount=amount, description=description, source=source, owner=request.user,
                                       date=date)
            else:
                Incomes.objects.create(amount=amount, description=description, source=source, owner=request.user)
            messages.success(request, 'Income saved successfully')
            return redirect('incomes')
        else:
            messages.error(request, 'Not all fields are filled')
            return render(request, template_name='incomes/add_incomes.html', context=context)


@login_required()
def edit_incomes(request, id):
    income = get_object_or_404(Incomes, pk=id)

    if request.user != income.owner:
        return HttpResponseForbidden()

    sources = Source.objects.all()
    context = {
        'user': request.user,
        'values': income,
        'sources': sources,
    }

    if request.method == 'GET':
        return render(request, template_name='incomes/edit_incomes.html', context=context)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        date = request.POST['date']
        if amount and description and source:
            income.amount = amount
            income.description = description
            income.source = source
            income.date = date
            income.save()
            messages.success(request, 'Income edit successfully')
            return redirect('incomes')
        else:
            messages.error(request, 'Not all fields are filled')
            return render(request, template_name='incomes/edit_incomes.html', context=context)


@login_required()
def delete_incomes(request, id):
    income = Incomes.objects.get(pk=id)

    if request.user != income.owner:
        return HttpResponseForbidden()

    income.delete()
    messages.success(request, 'Income successfully deleted')
    return redirect('incomes')


@login_required()
def search_incomes(request):
    data = request.POST['search_text']
    currency = get_object_or_404(UserPreference, user=request.user).currency
    if len(data) > 0:
        query_set = Incomes.objects.filter(Q(amount__icontains=data) & Q(owner=request.user)) | \
                    Incomes.objects.filter(Q(date__icontains=data) & Q(owner=request.user)) | \
                    Incomes.objects.filter(Q(description__icontains=data) & Q(owner=request.user)) | \
                    Incomes.objects.filter(Q(source__icontains=data) & Q(owner=request.user))
    else:
        query_set = Incomes.objects.filter(owner=request.user)[:4]
    context = {
        'user': request.user,
        'query_set': query_set,
        'currency': currency
    }
    return render(request, template_name='incomes/search.html', context=context)
