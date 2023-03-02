from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Expenses
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from userpreferences.models import UserPreference
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q

from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum

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
        query_set = Expenses.objects.filter(owner=request.user)
    context = {
        'user': request.user,
        'query_set': query_set,
        'currency': currency
    }
    return render(request, template_name='expenses/search.html', context=context)


@login_required()
def expenses_summary(request):
    currency = UserPreference.objects.get(user=request.user).currency
    if not currency:
        messages.info(request, 'Please choose your preferred currency')
        return redirect('preferences')

    all_expenses = Expenses.objects.filter(owner=request.user)
    today = datetime.datetime.today().date()
    today_data = {'amount': 0, 'count': 0}
    week_data = {'amount': 0, 'count': 0}
    month_data = {'amount': 0, 'count': 0}
    year_data = {'amount': 0, 'count': 0}
    week_ago = today - datetime.timedelta(days=7)
    month_ago = today - datetime.timedelta(days=30)
    year_ago = today - datetime.timedelta(days=365)

    for expense in all_expenses:
        if expense.date == today:
            today_data['amount'] += expense.amount
            today_data['count'] += 1

        if expense.date >= week_ago:
            week_data['amount'] += expense.amount
            week_data['count'] += 1

        if expense.date >= month_ago:
            month_data['amount'] += expense.amount
            month_data['count'] += 1

        if expense.date >= year_ago:
            year_data['amount'] += expense.amount
            year_data['count'] += 1

    context = {
        'currency': UserPreference.objects.get(user=request.user).currency.split('-')[0],
        'today': today_data,
        'this_week': week_data,
        'this_month': month_data,
        'this_year': year_data
    }

    return render(request, template_name='expenses/expenses_summary.html', context=context)


@login_required()
def expenses_summary_rest(request):
    all_expenses = Expenses.objects.filter(owner=request.user)
    today = datetime.datetime.today().date()
    today_amount = 0
    months_data = {}
    week_days_data = {}

    def get_amount_for_month(month):
        month_amount = 0
        for one in all_expenses:
            month_, year = one.date.month, one.date.year
            if month == month_ and year == today_year:
                month_amount += one.amount
        return month_amount

    for x in range(1, 13):
        today_month, today_year = x, datetime.datetime.today().year
        for one in all_expenses:
            months_data[x] = get_amount_for_month(x)

    def get_amount_for_day(x, today_day, month, today_year):
        day_amount = 0
        for one in all_expenses:
            day_, date_, month_, year_ = one.date.isoweekday(
            ), one.date.day, one.date.month, one.date.year
            if x == day_ and month == month_ and year_ == today_year:
                if not day_ > today_day:
                    day_amount += one.amount
        return day_amount

    for x in range(1, 8):
        today_day, today_month, today_year = datetime.datetime.today(
        ).isoweekday(), datetime.datetime.today(
        ).month, datetime.datetime.today().year
        for one in all_expenses:
            week_days_data[x] = get_amount_for_day(
                x, today_day, today_month, today_year)

    data = {"months": months_data, "days": week_days_data}
    return JsonResponse({'data_chart': {'all_data': data, 'nameChart': 'Expenses'}}, safe=False)


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


@login_required()
def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename="expenses_' + str(datetime.datetime.now()) + '.pdf"'
    response['Content-Transfer-Encoding'] = 'binary'

    expenses = Expenses.objects.filter(owner=request.user)
    sum_of_expense = expenses.aggregate(Sum('amount'))

    html_string = render_to_string('expenses/pdf-output.html', {'expenses': expenses, 'total': sum_of_expense['amount__sum']})
    html = HTML(string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()

        output = open(output.name, 'rb')
        response.write(output.read())

    return response


@login_required()
def last_3months_stats(request):
    todays_date = datetime.date.today()
    three_months_ago = datetime.date.today() - datetime.timedelta(days=90)
    expenses = Expenses.objects.filter(owner=request.user,
                                      date__gte=three_months_ago, date__lte=todays_date)

    def get_categories(item):
        return item.category
    final = {}
    categories = list(set(map(get_categories, expenses)))

    def get_expense_count(y):
        new = Expenses.objects.filter(category=y, owner=request.user)
        count = new.count()
        amount = 0
        for y in new:
            amount += y.amount
        return {'count': count, 'amount': amount}

    for x in expenses:
        for cat in categories:
            final[cat] = get_expense_count(cat)
    return JsonResponse({'category_data': final}, safe=False)


@login_required()
def last_3months_expense_source_stats(request):
    todays_date = datetime.date.today()
    last_month = datetime.date.today() - datetime.timedelta(days=0)
    last_2_month = last_month - datetime.timedelta(days=30)
    last_3_month = last_2_month - datetime.timedelta(days=30)

    last_month_income = Expenses.objects.filter(owner=request.user,
                                               date__gte=last_month, date__lte=todays_date).order_by('date')
    prev_month_income = Expenses.objects.filter(owner=request.user,
                                               date__gte=last_month, date__lte=last_2_month)
    prev_prev_month_income = Expenses.objects.filter(owner=request.user,
                                                    date__gte=last_2_month, date__lte=last_3_month)

    keyed_data = []
    this_month_data = {'7th': 0, '15th': 0, '22nd': 0, '29th': 0}
    prev_month_data = {'7th': 0, '15th': 0, '22nd': 0, '29th': 0}
    prev_prev_month_data = {'7th': 0, '15th': 0, '22nd': 0, '29th': 0}

    for x in last_month_income:
        date_in_month = str(x.date)[:2]
        if int(date_in_month) <= 7:
            this_month_data['7th'] += x.amount
        if 7 < int(date_in_month) <= 15:
            this_month_data['15th'] += x.amount
        if 16 <= int(date_in_month) <= 21:
            this_month_data['22nd'] += x.amount
        if 22 < int(date_in_month) < 31:
            this_month_data['29th'] += x.amount

    keyed_data.append({str(last_month): this_month_data})

    for x in prev_month_income:
        date_in_month = str(x.date)[:2]
        if int(date_in_month) <= 7:
            prev_month_data['7th'] += x.amount
        if 7 < int(date_in_month) <= 15:
            prev_month_data['15th'] += x.amount
        if 16 <= int(date_in_month) <= 21:
            prev_month_data['22nd'] += x.amount
        if 22 < int(date_in_month) < 31:
            prev_month_data['29th'] += x.amount

    keyed_data.append({str(last_2_month): prev_month_data})

    for x in prev_prev_month_income:
        date_in_month = str(x.date)[:2]
        if int(date_in_month) <= 7:
            prev_prev_month_data['7th'] += x.amount
        if 7 < int(date_in_month) <= 15:
            prev_prev_month_data['15th'] += x.amount
        if 16 <= int(date_in_month) <= 21:
            prev_prev_month_data['22nd'] += x.amount
        if 22 < int(date_in_month) < 31:
            prev_prev_month_data['29th'] += x.amount

    keyed_data.append({str(last_3_month): prev_month_data})
    return JsonResponse({'cumulative_income_data': keyed_data}, safe=False)
