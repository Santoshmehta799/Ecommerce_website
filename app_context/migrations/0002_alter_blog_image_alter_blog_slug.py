# Generated by Django 5.0 on 2024-01-23 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_context', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(upload_to='blogs'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]