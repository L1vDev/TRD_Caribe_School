# Generated by Django 5.1.6 on 2025-05-31 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_store', '0006_invoices_processed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoices',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha'),
        ),
    ]
