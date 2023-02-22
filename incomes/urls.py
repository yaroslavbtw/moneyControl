from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='incomes'),
    path('add-incomes/', add_incomes, name='add-incomes'),
    path('edit-incomes/<int:id>/', edit_incomes, name='edit-incomes'),
    path('delete-incomes/<int:id>/', delete_incomes, name='delete-incomes'),
    path('search-incomes/', search_incomes, name='search-incomes'),
    path('incomes_source_summary/', incomes_category_summary, name='incomes_category_summary'),
    path('incomes-summary/', incomes_summary, name='incomes_summary')
]
