from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from app_auth.utils import get_unique_filename
from django.conf import settings
from xhtml2pdf import pisa
from django.core.files.base import ContentFile
from django.template.loader import render_to_string
import io
import uuid
from django.contrib.staticfiles import finders
from private_storage.fields import PrivateFileField

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
    phone_number = models.CharField(verbose_name="Teléfono", blank=True, null=True,validators=[RegexValidator(regex=r'^\+\d{10,15}$', message="Introduzca un número de teléfono válido.")])
    province=models.CharField(verbose_name="Provincia",max_length=100)
    municipality=models.CharField(verbose_name="Municipio",max_length=100)
    address=models.CharField(verbose_name="Dirección",max_length=255)
    delivery_details=models.TextField(verbose_name="Detalles de Entrega", null=True, blank=True)
    delivery_price=models.DecimalField(verbose_name="Precio de Entrega",max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0.00)])
    status=models.CharField(verbose_name="Estado",max_length=50,default='pending',choices=STATUS_CHOICES)
    invoice_file=PrivateFileField(verbose_name="Factura", upload_to="invoices/")
    created_at=models.DateTimeField(auto_now_add=True,verbose_name="Fecha de Creación")

    def __str__(self):
        return f"Factura {self.id} - {self.first_name} {self.last_name}"
    
    def clean(self):
        super().clean()
        if not self.pk:
            return

        previous = Invoices.objects.get(pk=self.pk)
        prev_status = previous.status
        new_status = self.status

        if prev_status==new_status:
            return

        if prev_status == 'pending':
            return

        if new_status == 'pending':
            raise ValidationError("No se puede volver al estado 'Pendiente' desde otro estado.")

        if prev_status in ['sended', 'completed'] and new_status == 'canceled':
            raise ValidationError("No se puede cancelar una factura que ya fue enviada o completada.")

        if prev_status == 'canceled' and new_status != 'canceled':
            raise ValidationError("No se puede cambiar el estado de una factura cancelada.")
    
    def get_total_amount(self):
        total=0
        for product in self.products.all():
            total+=product.get_product_total()
        total+=self.delivery_price
        return total
    
    def generate_pdf(self):
        logo_pdf_url = finders.find("img/logo.png")
        context = {
            'invoice': self,
            'logo_pdf_url': logo_pdf_url,
            'products':self.products.all(),
        }
        html_ticket = render_to_string('utils/ticket_invoice.html', context)
        result_pdf = io.BytesIO() 
        
        pdf_file = pisa.pisaDocument(io.BytesIO(html_ticket.encode("UTF-8")), result_pdf)
        self.invoice_file.save(f'{str(self.id)}.pdf', ContentFile(result_pdf.getvalue()))
    
    def cancel_invoice(self):
        from app_products.models import Products
        self.status="canceled"
        for invoice_product in self.products.all():
            product,created=Products.objects.get_or_create(
                name=invoice_product.product_name,
                price=invoice_product.price,
                discount=invoice_product.product_discount
            )
            product.stock=product.stock+invoice_product.quantity
            product.save()
        self.save()

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
        return f"{self.product_name} - Factura {self.invoice.id}"
    
    def get_product_total(self):
        discount_price=self.product_price*(1-self.product_discount/100)
        product_total=discount_price*self.quantity
        return round(product_total,2)
    
    class Meta:
        verbose_name = 'Producto de Factura'
        verbose_name_plural = 'Productos de Factura'
        unique_together = ('invoice', 'product_id')

class Cart(models.Model):
    user = models.ForeignKey("app_auth.User", verbose_name='Usuario', on_delete=models.CASCADE)
    products = models.ManyToManyField("app_products.Products", verbose_name= 'Productos', through='CartItem', default=' ')
    is_active = models.BooleanField(verbose_name='Carrito Activo', default= True)

    def get_subtotal(self):
        subtotal=0
        for item in self.cartitem_set.all():
            subtotal += item.get_total()
        return subtotal

    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="Carrito")
    product = models.ForeignKey("app_products.Products", on_delete=models.CASCADE, verbose_name="Producto",null = True, blank=True, default=None)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Cantidad")

    def get_total(self):
        total=self.product.get_discount_price()*self.quantity
        return total
    
    def get_is_enough(self):
        return self.quantity<=self.product.stock

    class Meta:
        verbose_name = "Producto del carrito"
        verbose_name_plural = "Productos del carrito"
