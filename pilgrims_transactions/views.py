from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Transactions
from .serializers import TransactionsSerializer, TransactionValidationSerializer

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
    
    
    serializer = TransactionsSerializer(data=request.data)
    
    if serializer.is_valid():
        wilaya = serializer.validated_data["wilaya"]
        code = str(wilaya) + generate_payment_code()
        while Transactions.objects.filter(payment_code=code).exists():
            code = wilaya + generate_payment_code()
        
        
        if Transactions.objects.filter(nin=data['nin']).exists():
            return Response({"error": "NIN already exists"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(payment_code=code)
        return Response({"success": True}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def check_transaction(request):
    # here i need to validate using the nin and first name , last name, payment code
    data = request.data
    serializer = TransactionValidationSerializer(data=data)
    if serializer.is_valid():
        return Response({"success": True}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
