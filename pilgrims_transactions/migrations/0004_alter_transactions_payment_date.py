# Generated by Django 5.0.6 on 2024-05-08 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pilgrims_transactions', '0003_remove_transactions_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='payment_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]