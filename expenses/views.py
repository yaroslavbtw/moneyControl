from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Expenses
from django.http import HttpResponseForbidden
from userpreferences.models import UserPreference
from django.shortcuts import get_object_or_404


@login_required()
def index(request):
    user_expenses = Expenses.objects.filter(owner=request.user)
    user_preferences = get_object_or_404(UserPreference, user=request.user)
    # user_preferences = UserPreference.objects.get(user=request.user)
    context = {
        'user_expenses': user_expenses,
        'currency': user_preferences.currency
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
    categories = Category.objects.all()
    context = {
        'values': expense,
        'categories': categories,
    }
    if request.method == 'GET':
        if request.user != expense.owner:
            return HttpResponseForbidden()
        return render(request, template_name='expenses/expense-edit.html', context=context)
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
            return render(request, template_name='expenses/expense-edit.html', context=context)
