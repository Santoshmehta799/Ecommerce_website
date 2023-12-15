# Generated by Django 5.0 on 2023-12-15 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cities',
            old_name='city',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='states',
            old_name='state',
            new_name='name',
        ),
        migrations.AlterUniqueTogether(
            name='cities',
            unique_together={('state', 'name')},
        ),
    ]
