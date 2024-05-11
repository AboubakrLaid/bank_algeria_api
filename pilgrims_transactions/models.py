from django.db import models


class Transactions(models.Model):
    nin = models.CharField(max_length=18)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    wilaya = models.IntegerField()
    payment_code = models.CharField(max_length=10)
    payment_date = models.DateField(auto_now_add=True)
    file = models.FileField(upload_to='transactions/')
