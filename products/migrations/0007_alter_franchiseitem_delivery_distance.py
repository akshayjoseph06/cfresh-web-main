# Generated by Django 4.2.2 on 2023-07-24 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_remove_franchiseitem_variations_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='franchiseitem',
            name='delivery_distance',
            field=models.FloatField(default=0),
        ),
    ]
