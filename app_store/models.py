from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from app_auth.utils import get_unique_filename
import uuid

class Invoices(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('sended', 'Enviada'),
        ('completed', 'Completada'),
        ('canceled', 'Cancelada'),
    ]
    id=models.CharField(verbose_name="ID",primary_key=True,default=uuid.uuid4,editable=False)
    email=models.EmailField(verbose_name="Correo Electrónico")
    first_name=models.CharField(verbose_name="Nombre")
    last_name=models.CharField(verbose_name="Apellidos")
    phone = models.CharField(verbose_name="Teléfono", blank=True, null=True,validators=[RegexValidator(regex=r'^\+\d{10,15}$', message="Introduzca un número de teléfono válido.")])
    province=models.CharField(verbose_name="Provincia",max_length=100)
    municipality=models.CharField(verbose_name="Municipio",max_length=100)
    address=models.CharField(verbose_name="Dirección",max_length=255)
    delivery_price=models.DecimalField(verbose_name="Precio de Entrega",max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0.00)])
    status=models.CharField(verbose_name="Estado",max_length=50,default='Pendiente',choices=STATUS_CHOICES)
    invoice_file=models.FileField(verbose_name="Archivo de Factura", upload_to="invoices/")
    created_at=models.DateTimeField(auto_now_add=True,verbose_name="Fecha de Creación")

    def __str__(self):
        return f"Factura {self.id} - {self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['-created_at']

class InvoiceProducts(models.Model):
    invoice = models.ForeignKey(Invoices, verbose_name="Factura", on_delete=models.CASCADE, related_name='products')
    product_id= models.PositiveIntegerField(verbose_name="ID del Producto")
    product_name=models.CharField(verbose_name="Nombre del Producto")
    product_price=models.DecimalField(verbose_name="Precio del Producto", max_digits=15, decimal_places=2, default=0.00, validators=[MinValueValidator(0.00)])
    product_discount=models.DecimalField(verbose_name="Descuento del Producto", max_digits=15, decimal_places=2, default=0.00, validators=[MinValueValidator(0.00), MaxValueValidator(100.00)])
    quantity = models.PositiveIntegerField(verbose_name="Cantidad", default=1)

    def __str__(self):
        return f"{self.product.name} - Factura {self.invoice.id}"
    
    class Meta:
        verbose_name = 'Producto de Factura'
        verbose_name_plural = 'Productos de Factura'
        unique_together = ('invoice', 'product_id')

class Cart(models.Model):
    user = models.ForeignKey("app_auth.User", verbose_name='Usuario', on_delete=models.CASCADE)
    products = models.ManyToManyField("app_products.Products", verbose_name= 'Productos', through='CartItem', default=' ')
    is_active = models.BooleanField(verbose_name='Carrito Activo', default= True)

    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="Carrito")
    product = models.ForeignKey("app_products.Products", on_delete=models.CASCADE, verbose_name="Producto",null = True, blank=True, default=None)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Cantidad")

    def save(self, *args, **kwargs):
        MAX_CART_ITEMS = 40
        if self.cart.cartitem_set.count() >= MAX_CART_ITEMS and not self.pk:
            raise ValidationError(f'Cannot add more than {MAX_CART_ITEMS} items to the cart.')
        super(CartItem, self).save(*args, **kwargs)
    

    class Meta:
        verbose_name = "Producto del carrito"
        verbose_name_plural = "Productos del carrito"
