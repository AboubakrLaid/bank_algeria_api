from django.urls import path
from .views import add_transaction, get_transactions, check_transaction

urlpatterns = [
    
    path('all', get_transactions),
    path('new', add_transaction),
    path('check', check_transaction)
]
