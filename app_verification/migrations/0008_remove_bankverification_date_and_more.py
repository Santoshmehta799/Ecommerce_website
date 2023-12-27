# Generated by Django 5.0 on 2023-12-26 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_verification', '0007_bankverification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankverification',
            name='date',
        ),
        migrations.AlterField(
            model_name='bankverification',
            name='account_number',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='bankverification',
            name='beneficiary_id',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
        migrations.AlterField(
            model_name='bankverification',
            name='branch',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
        migrations.AlterField(
            model_name='bankverification',
            name='mobile',
            field=models.CharField(default='', max_length=13),
        ),
    ]