# Generated by Django 5.0 on 2023-12-26 13:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_inventory', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pickupwarehouselocation',
            options={'verbose_name': 'Inventory - Pickup Warehouse Location', 'verbose_name_plural': 'Inventory - Pickup Warehouse Location'},
        ),
        migrations.RemoveField(
            model_name='pickupwarehouselocation',
            name='city',
        ),
        migrations.RemoveField(
            model_name='pickupwarehouselocation',
            name='state',
        ),
        migrations.AlterField(
            model_name='pickupwarehouselocation',
            name='location_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='pickupwarehouselocation',
            name='plot_no',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='pickupwarehouselocation',
            name='street',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='pickupwarehouselocation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory_warehouse_location', to=settings.AUTH_USER_MODEL),
        ),
    ]