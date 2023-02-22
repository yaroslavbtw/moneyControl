from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='expenses'),
    path('add-expenses/', add_expenses, name='add-expenses'),
    path('edit-expenses/<int:id>/', edit_expanses, name='edit-expenses'),
    path('delete-expenses/<int:id>/', delete_expenses, name='delete-expenses'),
    path('search-expenses/', search_expense, name='search-expenses'),
    path('expenses_category_summary/', expenses_category_summary, name='expenses_category_summary'),
    path('expenses-summary/', expenses_summary, name='expenses_summary'),
    path('export-csv/', export_csv, name='expenses-export-csv'),
    path('export-excel/', export_excel, name='expenses-export-excel'),
]
