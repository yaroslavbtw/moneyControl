from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Incomes, Source
from django.http import HttpResponseForbidden, JsonResponse
from userpreferences.models import UserPreference
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q
import datetime


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


@login_required()
def incomes_summary(request):
    if not UserPreference.objects.filter(user=request.user).exists():
        messages.info(request, 'Please choose your preferred currency')
        return redirect('preferences')

    all_incomes = Incomes.objects.filter(owner=request.user)
    today = datetime.datetime.today().date()
    today_data = {'amount': 0, 'count': 0}
    week_data = {'amount': 0, 'count': 0}
    month_data = {'amount': 0, 'count': 0}
    year_data = {'amount': 0, 'count': 0}
    week_ago = today - datetime.timedelta(days=7)
    month_ago = today - datetime.timedelta(days=30)
    year_ago = today - datetime.timedelta(days=365)

    for income in all_incomes:
        if income.date == today:
            today_data['amount'] += income.amount
            today_data['count'] += 1

        if income.date >= week_ago:
            week_data['amount'] += income.amount
            week_data['count'] += 1

        if income.date >= month_ago:
            month_data['amount'] += income.amount
            month_data['count'] += 1

        if income.date >= year_ago:
            year_data['amount'] += income.amount
            year_data['count'] += 1

    context = {
        'currency': UserPreference.objects.get(user=request.user).currency.split('-')[0],
        'today': today_data,
        'this_week': week_data,
        'this_month': month_data,
        'this_year': year_data
    }

    return render(request, template_name='incomes/incomes_summary.html', context=context)


@login_required()
def incomes_summary_rest(request):
    all_incomes = Incomes.objects.filter(owner=request.user)
    today = datetime.datetime.today().date()
    today_amount = 0
    months_data = {}
    week_days_data = {}

    def get_amount_for_month(month):
        month_amount = 0
        for one in all_incomes:
            month_, year = one.date.month, one.date.year
            if month == month_ and year == today_year:
                month_amount += one.amount
        return month_amount

    for x in range(1, 13):
        today_month, today_year = x, datetime.datetime.today().year
        for one in all_incomes:
            months_data[x] = get_amount_for_month(x)

    def get_amount_for_day(x, today_day, month, today_year):
        day_amount = 0
        for one in all_incomes:
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
        for one in all_incomes:
            week_days_data[x] = get_amount_for_day(
                x, today_day, today_month, today_year)

    data = {"months": months_data, "days": week_days_data}
    return JsonResponse({'data_chart': {'all_data': data, 'nameChart': 'Incomes'}}, safe=False)


@login_required()
def last_3months_income_stats(request):
    todays_date = datetime.date.today()
    three_months_ago = datetime.date.today() - datetime.timedelta(days=90)
    income = Incomes.objects.filter(owner=request.user, date__gte=three_months_ago, date__lte=todays_date)

    def get_sources(item):
        return item.source
    final = {}
    sources = list(set(map(get_sources, income)))

    def get_sources_count(y):
        new = Incomes.objects.filter(source=y)
        count = new.count()
        amount = 0
        for y in new:
            amount += y.amount
        return {'count': count, 'amount': amount}

    for x in income:
        for y in sources:
            final[y] = get_sources_count(y)
    return JsonResponse({'category_data': final}, safe=False)


@login_required()
def last_3months_income_source_stats(request):
    todays_date = datetime.date.today()
    last_month = datetime.date.today() - datetime.timedelta(days=0)
    last_2_month = last_month - datetime.timedelta(days=30)
    last_3_month = last_2_month - datetime.timedelta(days=30)

    last_month_income = Incomes.objects.filter(owner=request.user, date__gte=last_month,
                                               date__lte=todays_date).order_by('date')
    prev_month_income = Incomes.objects.filter(owner=request.user, date__gte=last_month, date__lte=last_2_month)
    prev_prev_month_income = Incomes.objects.filter(owner=request.user, date__gte=last_2_month, date__lte=last_3_month)

    keyed_data = []
    this_month_data = {'7th': 0, '15th': 0, '22nd': 0, '29th': 0}
    prev_month_data = {'7th': 0, '15th': 0, '22nd': 0, '29th': 0}
    prev_prev_month_data = {'7th': 0, '15th': 0, '22nd': 0, '29th': 0}

    for x in last_month_income:
        month = str(x.date)[:7]
        date_in_month = str(x.date)[:2]
        if int(date_in_month) <= 7:
            this_month_data['7th'] += x.amount
        if int(date_in_month) > 7 and int(date_in_month) <= 15:
            this_month_data['15th'] += x.amount
        if int(date_in_month) >= 16 and int(date_in_month) <= 21:
            this_month_data['22nd'] += x.amount
        if int(date_in_month) > 22 and int(date_in_month) < 31:
            this_month_data['29th'] += x.amount

    keyed_data.append({str(last_month): this_month_data})

    for x in prev_month_income:
        date_in_month = str(x.date)[:2]
        month = str(x.date)[:7]
        if int(date_in_month) <= 7:
            prev_month_data['7th'] += x.amount
        if int(date_in_month) > 7 and int(date_in_month) <= 15:
            prev_month_data['15th'] += x.amount
        if int(date_in_month) >= 16 and int(date_in_month) <= 21:
            prev_month_data['22nd'] += x.amount
        if int(date_in_month) > 22 and int(date_in_month) < 31:
            prev_month_data['29th'] += x.amount

    keyed_data.append({str(last_2_month): prev_month_data})

    for x in prev_prev_month_income:
        date_in_month = str(x.date)[:2]
        month = str(x.date)[:7]
        if int(date_in_month) <= 7:
            prev_prev_month_data['7th'] += x.amount
        if int(date_in_month) > 7 and int(date_in_month) <= 15:
            prev_prev_month_data['15th'] += x.amount
        if int(date_in_month) >= 16 and int(date_in_month) <= 21:
            prev_prev_month_data['22nd'] += x.amount
        if int(date_in_month) > 22 and int(date_in_month) < 31:
            prev_prev_month_data['29th'] += x.amount

    keyed_data.append({str(last_3_month): prev_month_data})
    return JsonResponse({'cumulative_income_data': keyed_data}, safe=False)
