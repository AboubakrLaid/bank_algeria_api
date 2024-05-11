from django.urls import path
from .views import add_transaction, get_transactions

urlpatterns = [
    
    path('all', get_transactions),
    path('new', add_transaction),
]
