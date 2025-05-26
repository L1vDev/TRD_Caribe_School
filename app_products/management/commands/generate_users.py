# tu_app/management/commands/create_users.py
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from app_auth.models import User
import uuid

class Command(BaseCommand):
    help = 'Crea 700 usuarios de prueba con configuración específica'

    def handle(self, *args, **options):
        base_email = "usuario{}@ejemplo.com"  # Plantilla para emails únicos
        password = "pass"  # Contraseña común para todos
        
        for i in range(1, 701):
            email = base_email.format(i)
            
            User.objects.create(
                email=email,
                first_name="Nombre",  # Mismo nombre para todos
                last_name="Apellido",  # Mismo apellido para todos
                password=make_password(password),  # Hashear la contraseña
                phone_number="+5352735874",
                is_email_verified=True,
                is_active=True,
                is_staff=False,
                is_superuser=False,
                # phone_number y profile_picture se omiten (null por defecto)
            )
            
            self.stdout.write(f'Usuario {i}/700 creado: {email}')

        self.stdout.write(self.style.SUCCESS('\n¡700 usuarios creados exitosamente!'))