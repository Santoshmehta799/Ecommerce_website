# Generated by Django 5.0 on 2024-01-30 08:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_dashboard', '0001_initial'),
        ('app_inventory', '0015_alter_pricestructure_hsn_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pickupwarehouselocation',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app_dashboard.cities'),
        ),
        migrations.AlterField(
            model_name='pickupwarehouselocation',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app_dashboard.states'),
        ),
    ]
