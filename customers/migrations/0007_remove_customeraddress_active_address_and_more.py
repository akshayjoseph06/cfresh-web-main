# Generated by Django 4.2.2 on 2023-08-02 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0006_alter_customer_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customeraddress',
            name='active_address',
        ),
        migrations.AlterField(
            model_name='customeraddress',
            name='address_type',
            field=models.CharField(max_length=2),
        ),
    ]
