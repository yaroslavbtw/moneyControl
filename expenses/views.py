from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Expenses
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from userpreferences.models import UserPreference
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q
import datetime
import csv
import xlwt


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
        'user': request.user,
        'currency': user_preferences.currency,
        'page_obj': page_object,
        'page_obj_length': len(page_object.object_list)
    }
    return render(request, template_name='expenses/index.html', context=context)


@login_required()
def add_expenses(request):
    categories = Category.objects.all()
    context = {
        'user': request.user,
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
        'user': request.user,
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
        'user': request.user,
        'query_set': query_set,
        'currency': currency
    }
    return render(request, template_name='expenses/search.html', context=context)


@login_required()
def expenses_summary(request):
    return render(request, template_name='expenses/expenses_summary.html')


@login_required()
def expenses_category_summary(request):
    today = datetime.datetime.today()
    six_month_ago = today - datetime.timedelta(days=30*6)
    expenses = Expenses.objects.filter(date__gte=six_month_ago, date__lte=today, owner=request.user)

    final_rep = {}

    def get_category(exp):
        return exp.category

    def get_expense_category_amount(cat):
        amount = 0
        query_set = expenses.filter(category=cat)
        for exp in query_set:
            amount += exp.amount
        return amount

    category_list = list(set(map(get_category, expenses)))
    for expense in expenses:
        for category in category_list:
            final_rep[category] = get_expense_category_amount(category)

    return JsonResponse({'category_data': final_rep, 'nameChart': 'Expenses'}, safe=False)


@login_required()
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses_' + str(datetime.datetime.now()) + '.csv"'
    try:
        currency = get_object_or_404(UserPreference, user=request.user).currency
    except UserPreference.DoesNotExist:
        currency = ''
    writer = csv.writer(response)
    writer.writerow(['Amount(' + currency + ')', 'Category', 'Description', 'Date'])

    expenses = Expenses.objects.filter(owner=request.user)
    for expense in expenses:
        writer.writerow([expense.amount, expense.category, expense.description, expense.date])
    return response


@login_required()
def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="expenses_' + str(datetime.datetime.now()) + '.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    try:
        currency = get_object_or_404(UserPreference, user=request.user).currency
    except UserPreference.DoesNotExist:
        currency = ''

    columns = ['Amount(' + currency + ')', 'Category', 'Description', 'Date']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = Expenses.objects.filter(owner=request.user).values_list('amount', 'category', 'description', 'date')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)
    return response
