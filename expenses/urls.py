from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='expenses'),
    path('add-expenses/', add_expenses, name='add-expenses'),
    path('edit-expenses/<int:id>/', edit_expanses, name='edit-expenses'),
    path('delete-expenses/<int:id>/', delete_expenses, name='delete-expenses'),
    path('search-expenses/', search_expense, name='search-expenses'),
    path('expenses-summary-rest/', expenses_summary_rest, name='expenses-summary-rest'),
    path('expenses-summary/', expenses_summary, name='expenses_summary'),
    path('export-csv/', export_csv, name='expenses-export-csv'),
    path('export-excel/', export_excel, name='expenses-export-excel'),
    path('export-pdf/', export_pdf, name='expenses-export-pdf'),
    path('three_months_summary/', last_3months_stats, name='three_months_summary'),
    path('last_3months_expense_source_stats/', last_3months_expense_source_stats,
         name="last_3months_expense_source_stats")
]
