# Generated by Django 4.2.2 on 2023-07-15 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0001_initial'),
        ('products', '0002_franchiseitem_gross_weight_franchiseitem_net_weight_and_more'),
        ('customers', '0002_customeraddress_alter_customer_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='bag_value',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customer',
            name='wallet_amount',
            field=models.FloatField(default=0),
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now=True)),
                ('quantity', models.IntegerField(default=1)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
                ('flash_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='promotions.flashsaleitems')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.franchiseitem')),
                ('today_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='promotions.todaydealitems')),
                ('varient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.variantdetail')),
            ],
            options={
                'verbose_name': 'cart',
                'verbose_name_plural': 'carts',
                'db_table': 'customer_cart',
                'ordering': ('-id',),
            },
        ),
    ]
