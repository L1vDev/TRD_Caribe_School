# tu_app/management/commands/generate_products.py
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from app_products.models import Products, Category
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Genera 100 productos de prueba'

    def handle(self, *args, **kwargs):
        fake = Faker('es_ES')  # Configura Faker para datos en español
        Faker.seed(0)
        
        # Crear algunas categorías si no existen
        Category.objects.get_or_create(name="Electrónica")
        Category.objects.get_or_create(name="Hogar")
        categorias = Category.objects.all()
        
        for _ in range(100):
            nombre = fake.unique.company()
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
            
            # Añadir categorías aleatorias
            producto.category.add(*categorias)
            
            self.stdout.write(self.style.SUCCESS(f'Producto creado: {nombre}'))

        self.stdout.write(self.style.SUCCESS('\n¡30 productos creados exitosamente!'))