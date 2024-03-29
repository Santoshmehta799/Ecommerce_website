# Generated by Django 5.0 on 2024-01-08 11:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_inventory', '0003_rename_default_varient_productvariant_default_variant_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pricestructure',
            old_name='mpr',
            new_name='mrp',
        ),
        migrations.AlterField(
            model_name='producttype',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_types', to='app_inventory.category'),
        ),
        migrations.AlterField(
            model_name='shippingdetails',
            name='product_dimensions_unit',
            field=models.CharField(blank=True, choices=[('piece', 'Piece'), ('bag', 'Bag'), ('metric_tonne', 'Metric Tonne'), ('kilogram', 'Kilogram'), ('cubic_foot', 'Cubic Foot'), ('square_foot', 'Square Foot'), ('cubic_meter', 'Cubic Meter'), ('meter', 'Meter'), ('set', 'Set'), ('litre', 'Litre'), ('foot', 'Foot'), ('bundle', 'Bundle'), ('square_meter', 'Square Meter')], max_length=50, null=True),
        ),
    ]
