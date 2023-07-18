# Generated by Django 4.2.2 on 2023-06-25 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('franchise', '0004_franchise_base_charge_franchise_base_distance_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('image', models.FileField(upload_to='category')),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'db_table': 'product_category',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='ItemVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'item variant',
                'verbose_name_plural': 'item variants',
                'db_table': 'product_item_variant',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='VariantDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('image', models.FileField(upload_to='item')),
                ('unit', models.CharField(max_length=10)),
                ('unit_quantity', models.FloatField(default=1)),
                ('per_unit_price', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('item_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.itemvariant')),
            ],
            options={
                'verbose_name': 'variant detail',
                'verbose_name_plural': 'variant details',
                'db_table': 'product_variant_detail',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('image', models.FileField(upload_to='item')),
                ('description', models.CharField(max_length=999)),
                ('is_active', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.category')),
            ],
            options={
                'verbose_name': 'item',
                'verbose_name_plural': 'items',
                'db_table': 'product_item',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='FranchiseItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now=True)),
                ('unit', models.CharField(max_length=10)),
                ('unit_quantity', models.FloatField(default=1)),
                ('per_unit_price', models.IntegerField()),
                ('sold', models.IntegerField(default=0)),
                ('in_stock', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('franchise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='franchise.franchise')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.item')),
                ('variations', models.ManyToManyField(to='products.variantdetail')),
            ],
            options={
                'verbose_name': 'franchise item',
                'verbose_name_plural': 'franchise items',
                'db_table': 'product_franchise_item',
                'ordering': ('-id',),
            },
        ),
    ]
