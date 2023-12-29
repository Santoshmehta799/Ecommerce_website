# Generated by Django 5.0 on 2023-12-28 11:43

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_inventory', '0003_remove_pickupwarehouselocation_pincode_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('created_by', models.UUIDField(blank=True, help_text='User Id who created this record.', null=True)),
                ('updated_by', models.UUIDField(blank=True, help_text='User Id who updated this record.', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date and time at which this record is created', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date and time at which this record is last updated.', null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('image', models.ImageField(blank=True, default='', null=True, upload_to='category')),
                ('slug', models.SlugField(blank=True, max_length=140, null=True, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('created_by', models.UUIDField(blank=True, help_text='User Id who created this record.', null=True)),
                ('updated_by', models.UUIDField(blank=True, help_text='User Id who updated this record.', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date and time at which this record is created', null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date and time at which this record is last updated.', null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.ImageField(blank=True, default='', null=True, upload_to='product_type')),
                ('commission_type', models.CharField(max_length=25)),
                ('commission_value', models.IntegerField(blank=True, default=0)),
                ('returnable_product', models.BooleanField(default=False, null=True)),
                ('slug', models.SlugField(blank=True, max_length=140, null=True, unique=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='app_inventory.category')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
