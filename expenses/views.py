from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Expenses
from django.http import HttpResponseForbidden
from userpreferences.models import UserPreference
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q


@login_required()
def index(request):
    user_expenses = Expenses.objects.filter(owner=request.user)
    user_preferences = get_object_or_404(UserPreference, user=request.user)

    paginator = Paginator(user_expenses, 4)
    page_number = request.GET.get('page')
    if page_number:
        page_object = paginator.get_page(page_number)
    else:
        page_object = paginator.get_page(1)
    context = {
        'currency': user_preferences.currency,
        'page_obj': page_object,
        'page_obj_length': len(page_object.object_list)
    }
    return render(request, template_name='expenses/index.html', context=context)


@login_required()
def add_expenses(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, template_name='expenses/add_expenses.html', context=context)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['date']
        if amount and description and category:
            if date:
                Expenses.objects.create(amount=amount, description=description, category=category, owner=request.user,
                                        date=date)
            else:
                Expenses.objects.create(amount=amount, description=description, category=category, owner=request.user)
            messages.success(request, 'Expense saved successfully')
            return redirect('expenses')
        else:
            messages.error(request, 'Not all fields are filled')
            return render(request, template_name='expenses/add_expenses.html', context=context)


@login_required()
def edit_expanses(request, id):
    expense = get_object_or_404(Expenses, pk=id)

    if request.user != expense.owner:
        return HttpResponseForbidden()

    categories = Category.objects.all()
    context = {
        'values': expense,
        'categories': categories,
    }

    if request.method == 'GET':
        return render(request, template_name='expenses/edit_expense.html', context=context)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['date']
        if amount and description and category:
            expense.amount = amount
            expense.description = description
            expense.category = category
            expense.date = date
            expense.save()
            messages.success(request, 'Expense edit successfully')
            return redirect('expenses')
        else:
            messages.error(request, 'Not all fields are filled')
            return render(request, template_name='expenses/edit_expense.html', context=context)


@login_required()
def delete_expenses(request, id):
    expense = Expenses.objects.get(pk=id)

    if request.user != expense.owner:
        return HttpResponseForbidden()

    expense.delete()
    messages.success(request, 'Expense successfully deleted')
    return redirect('expenses')


@login_required()
def search_expense(request):
    data = request.POST['search_text']
    currency = get_object_or_404(UserPreference, user=request.user).currency
    if len(data) > 0:
        query_set = Expenses.objects.filter(Q(amount__icontains=data) & Q(owner=request.user)) | \
                    Expenses.objects.filter(Q(date__icontains=data) & Q(owner=request.user)) | \
                    Expenses.objects.filter(Q(description__icontains=data) & Q(owner=request.user)) | \
                    Expenses.objects.filter(Q(category__icontains=data) & Q(owner=request.user))
    else:
        query_set = Expenses.objects.filter(owner=request.user)[:4]
    context = {
        'query_set': query_set,
        'currency': currency
    }
    return render(request, template_name='expenses/search.html', context=context)
