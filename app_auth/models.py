from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from app_auth.utils import get_unique_filename
import uuid
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id=models.CharField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name="Correo Electrónico",unique=True)
    first_name = models.CharField(verbose_name="Nombre")
    last_name = models.CharField(verbose_name="Apellidos")
    phone_number = models.CharField(verbose_name="Teléfono",blank=True, null=True, validators=[RegexValidator(regex=r'^\+\d{10,15}$',message="Introduzca un número de teléfono válido.")])
    profile_picture= models.ImageField(verbose_name="Foto de Perfil",upload_to=get_unique_filename,null=True,blank=True)
    created_at = models.DateTimeField(verbose_name="Fecha de Creado",auto_now_add=True)
    is_email_verified = models.BooleanField(verbose_name="Correo Verificado",default=False)
    is_active = models.BooleanField(verbose_name="Activo",default=True)
    is_staff = models.BooleanField(verbose_name="Staff",default=False)
    is_superuser = models.BooleanField(verbose_name="Superusuario",default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def clean(self):
        if not self.first_name or not self.first_name.strip():
            raise ValidationError({'first_name':"El nombre no puede estar vacío."})
        if not self.last_name or not self.last_name.strip():
            raise ValidationError({'first_name':"El apellido no puede estar vacío."})
    
    def save(self, *args, **kwargs):
        self.full_clean()
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