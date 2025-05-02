from django.db import models
from django.core.validators import MinValueValidator, RegexValidator

class Province(models.Model):
    name = models.CharField(verbose_name="Provincia", unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'

class Municipality(models.Model):
    name = models.CharField(verbose_name="Municipio")
    province = models.ForeignKey(Province,verbose_name="Provincia", on_delete=models.CASCADE, related_name='municipalities')
    price= models.DecimalField(verbose_name="Precio",max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0.00)])

    def __str__(self):
        return f"{self.province.name}|{self.name}"
    
    class Meta:
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'
        unique_together = ('name', 'province')

class ContactRequest(models.Model):
    first_name = models.CharField(verbose_name="Nombre")
    last_name = models.CharField(verbose_name="Apellidos")
    email = models.EmailField(verbose_name="Correo Electrónico")
    phone_number = models.CharField(verbose_name="Teléfono", blank=True, null=True,validators=[RegexValidator(regex=r'^\+\d{10,15}$', message="Introduzca un número de teléfono válido.")])
    message = models.TextField(verbose_name="Mensaje")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Fecha de Solicitud")
    answered = models.BooleanField(default=False, verbose_name="Atendida")

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
    
    class Meta:
        verbose_name = 'Petición de Contacto'
        verbose_name_plural = 'Peticiones de Contacto'
    
