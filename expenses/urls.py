from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='expenses'),
    path('add-expenses/', add_expenses, name='add-expenses'),
    path('edit-expenses/<int:id>/', edit_expanses, name='edit-expenses'),
    path('delete-expenses/<int:id>/', delete_expenses, name='delete-expenses'),
    path('search-expenses/', search_expense, name='search-expenses')
]
