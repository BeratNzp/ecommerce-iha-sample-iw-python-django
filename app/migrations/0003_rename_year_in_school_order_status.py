# Generated by Django 5.0.4 on 2024-05-06 22:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_rename_is_deleted_stock_is_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='year_in_school',
            new_name='status',
        ),
    ]
