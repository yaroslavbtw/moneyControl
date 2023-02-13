from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='expenses'),
    path('add-expenses/', views.add_expenses, name='add-expenses'),
    path('edit-expenses/<int:id>/', views.edit_expanses, name='edit-expenses'),
    path('delete-expenses/<int:id>/', views.delete_expenses, name='delete-expenses'),
    path('search-expenses/', views.search_expense, name='search-expenses')
]
