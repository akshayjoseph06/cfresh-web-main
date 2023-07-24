# Generated by Django 4.2.2 on 2023-07-24 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_remove_customeraddress_block_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.ManyToManyField(blank=True, related_name='customer_address', to='customers.customeraddress'),
        ),
    ]
