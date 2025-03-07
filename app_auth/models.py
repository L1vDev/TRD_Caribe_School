from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False)
    dni_number = models.CharField(verbose_name="Carnet de Identidad",unique=True)
    email = models.EmailField(verbose_name="Correo Electrónico",unique=True)
    first_name = models.CharField(verbose_name="Nombre")
    last_name = models.CharField(verbose_name="Apellidos")
    phone_number = models.CharField(verbose_name="Teléfono",blank=True, null=True)
    #profile_picture
    #province
    #municipality
    address = models.CharField(verbose_name="Dirección Particular")
    created_at = models.DateTimeField(verbose_name="Creado",auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Actualizado",auto_now=True)
    is_email_verified = models.BooleanField(verbose_name="Correo Verificado",default=False)
    is_active = models.BooleanField(verbose_name="Activo",default=True)
    is_staff = models.BooleanField(verbose_name="Staff",default=False)
    is_superuser = models.BooleanField(verbose_name="Superusuario",default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','dni_number','address']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_staff = True
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

class Worker(User):
    class Meta:
        verbose_name = "Trabajador"
        verbose_name_plural = "Trabajadores"
        proxy = True   