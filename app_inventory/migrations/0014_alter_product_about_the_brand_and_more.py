# Generated by Django 5.0 on 2024-01-29 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_inventory', '0013_alter_product_product_title_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='about_the_brand',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_brand',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_title',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, max_length=1000, null=True),
        ),
    ]
