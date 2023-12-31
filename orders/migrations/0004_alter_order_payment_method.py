# Generated by Django 4.2.2 on 2023-08-14 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_options_alter_order_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('COD', 'Cash on Delivery'), ('PTM', 'Paytm'), ('WLT', 'Wallet')], max_length=3, null=True),
        ),
    ]
