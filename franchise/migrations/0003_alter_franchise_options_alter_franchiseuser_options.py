# Generated by Django 4.2.2 on 2023-06-14 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('franchise', '0002_franchise_franchiseuser_franchise'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='franchise',
            options={'ordering': ('-id',), 'verbose_name': 'franchise', 'verbose_name_plural': 'franchises'},
        ),
        migrations.AlterModelOptions(
            name='franchiseuser',
            options={'ordering': ('-id',), 'verbose_name': 'franchise user', 'verbose_name_plural': 'franchise users'},
        ),
    ]