# Generated by Django 5.0 on 2024-01-11 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_inventory', '0007_alter_productvariant_name_alter_productvariant_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariant',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='value',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
