# Generated by Django 5.1.6 on 2025-05-31 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_store', '0005_alter_invoices_invoice_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoices',
            name='processed',
            field=models.BooleanField(default=False, verbose_name='Estadística Procesada'),
        ),
    ]
