from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Transactions
from .serializers import TransactionsSerializer

import random


def generate_payment_code():
    length = 8
    string = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    x = ''.join(random.choice(string) for i in range(length))
    print(x)
    return x



@api_view(['GET'])
def get_transactions(request):
    transactions = Transactions.objects.all()
    serializer = TransactionsSerializer(transactions, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_transaction(request):
    data = request.data
    code = str(data["wilaya"]) + generate_payment_code()
    while Transactions.objects.filter(payment_code=code).exists():
        code = data["wilaya"] + generate_payment_code()
        
    data["payment_code"] = code
    print(len(code))
        
    if Transactions.objects.filter(nin=data['nin']).exists():
        return Response({"error": "NIN already exists"}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = TransactionsSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"success": True}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
