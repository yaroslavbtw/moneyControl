from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='expenses'),
    path('add-expenses/', views.add_expenses, name='add-expenses'),
    path('edit-expense/<int:id>/', views.edit_expanses, name='edit-expenses'),
    path('delete-expense/<int:id>/', views.delete_expenses, name='delete-expenses')
]
