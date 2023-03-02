from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='incomes'),
    path('add-incomes/', add_incomes, name='add-incomes'),
    path('edit-incomes/<int:id>/', edit_incomes, name='edit-incomes'),
    path('delete-incomes/<int:id>/', delete_incomes, name='delete-incomes'),
    path('search-incomes/', search_incomes, name='search-incomes'),
    path('incomes-summary-rest/', incomes_summary_rest, name='incomes_summary_rest'),
    path('incomes-summary/', incomes_summary, name='incomes_summary'),
    path('export-csv/', export_csv, name='incomes-export-csv'),
    path('export-excel/', export_excel, name='incomes-export-excel'),
    path('export-pdf/', export_pdf, name='incomes-export-pdf'),
    path('three_months_summary/', last_3months_income_stats, name='three_months_summary_'),
    path('last_3months_income_source_stats/', last_3months_income_source_stats,
         name='last_3months_income_source_stats_'),
]
