# Generated by Django 5.0 on 2024-01-11 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_inventory', '0005_remove_shippingdetails_pick_up_location_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='hsn_code',
        ),
        migrations.AddField(
            model_name='pricestructure',
            name='hsn_code',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='pricestructure',
            name='tax_code',
            field=models.CharField(blank=True, choices=[('0', '0%'), ('5', '5%'), ('12', '12%'), ('18', '18%'), ('28', '28%')], max_length=100, null=True),
        ),
    ]