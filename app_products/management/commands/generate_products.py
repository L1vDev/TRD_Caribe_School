# tu_app/management/commands/generate_products.py
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from app_products.models import Products, Category
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Genera 100 productos de prueba para una tienda virtual'

    def handle(self, *args, **kwargs):
        fake = Faker('es_ES')  # Configura Faker para datos en español
        Faker.seed(0)

        # Definir categorías típicas de una tienda virtual
        categorias_nombres = [
            "Electrónica", "Hogar", "Ropa", "Juguetes", "Deportes",
            "Libros", "Belleza", "Automotriz", "Mascotas", "Jardín"
        ]
        # Crear categorías si no existen
        for nombre in categorias_nombres:
            Category.objects.get_or_create(name=nombre)
        categorias = list(Category.objects.all())

        for _ in range(100):
            nombre = fake.unique.catch_phrase()
            canon = slugify(nombre)
            producto = Products.objects.create(
                name=nombre,
                canon_name=canon,
                price=Decimal(random.uniform(1.99, 999.99)).quantize(Decimal('0.00')),
                discount=Decimal(random.uniform(0.00, 100.00)).quantize(Decimal('0.00')),
                about=fake.paragraph(nb_sentences=5),
                details="\n".join(fake.sentences(nb=3)),
                stock=random.randint(0, 1000),
                available=True
            )

            # Asignar entre 1 y 3 categorías aleatorias
            num_categorias = random.randint(1, 3)
            categorias_aleatorias = random.sample(categorias, num_categorias)
            producto.category.add(*categorias_aleatorias)

            self.stdout.write(self.style.SUCCESS(f'Producto creado: {nombre}'))

        self.stdout.write(self.style.SUCCESS('\n¡100 productos creados exitosamente!'))