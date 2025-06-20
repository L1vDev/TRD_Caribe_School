# Generated by Django 5.1.6 on 2025-05-02 20:17

import app_auth.utils
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True, verbose_name='Nombre de la Categoría')),
            ],
            options={
                'verbose_name': 'Categoría',
                'verbose_name_plural': 'Categorías',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True, verbose_name='Nombre del Producto')),
                ('canon_name', models.CharField(verbose_name='Nombre Canónico')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Precio')),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)], verbose_name='Descuento')),
                ('about', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('details', models.TextField(blank=True, null=True, verbose_name='Detalles')),
                ('main_image', models.ImageField(blank=True, null=True, upload_to=app_auth.utils.get_unique_filename, verbose_name='Imagen')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='Stock')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='Vistas')),
                ('purchases', models.PositiveIntegerField(default=0, verbose_name='Compras')),
                ('public', models.BooleanField(default=False, verbose_name='Público')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('category', models.ManyToManyField(blank=True, related_name='products', to='app_products.category', verbose_name='Categoría')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=app_auth.utils.get_unique_filename, verbose_name='Imagen')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='app_products.products', verbose_name='Producto')),
            ],
            options={
                'verbose_name': 'Imagen del Producto',
                'verbose_name_plural': 'Imágenes del Producto',
            },
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Calificación')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comentario')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='app_products.products', verbose_name='Producto')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Reseña',
                'verbose_name_plural': 'Reseñas',
                'ordering': ['-created_at'],
                'unique_together': {('product', 'user')},
            },
        ),
    ]
