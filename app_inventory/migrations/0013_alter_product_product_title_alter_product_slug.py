# Generated by Django 5.0 on 2024-01-29 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_inventory', '0012_alter_producttype_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_title',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, max_length=225, null=True),
        ),
    ]
