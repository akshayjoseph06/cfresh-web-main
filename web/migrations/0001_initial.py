# Generated by Django 4.2.2 on 2023-07-04 14:23

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', ckeditor.fields.RichTextField()),
            ],
            options={
                'verbose_name': 'about',
                'verbose_name_plural': 'abouts',
                'db_table': 'cfresh_about',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('mob', models.BigIntegerField()),
                ('message', models.TextField()),
            ],
            options={
                'verbose_name': 'contact',
                'verbose_name_plural': 'contacts',
                'db_table': 'cfresh_contact',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ios', models.CharField(max_length=255)),
                ('android', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'link',
                'verbose_name_plural': 'links',
                'db_table': 'cfresh_link',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Privacy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', ckeditor.fields.RichTextField()),
            ],
            options={
                'verbose_name': 'privacy',
                'verbose_name_plural': 'privacy',
                'db_table': 'cfresh_privacy',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Return',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', ckeditor.fields.RichTextField()),
            ],
            options={
                'verbose_name': 'return',
                'verbose_name_plural': 'return',
                'db_table': 'cfresh_return',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Terms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', ckeditor.fields.RichTextField()),
            ],
            options={
                'verbose_name': 'terms',
                'verbose_name_plural': 'terms',
                'db_table': 'cfresh_terms',
                'ordering': ['-id'],
            },
        ),
    ]
