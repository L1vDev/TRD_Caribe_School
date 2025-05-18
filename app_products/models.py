from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from app_auth.utils import get_unique_filename
from django.utils import timezone

class Category(models.Model):
    name= models.CharField(verbose_name="Nombre de la Categoría", unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']

class Products(models.Model):
    name=models.CharField(verbose_name="Nombre del Producto",unique=True)
    canon_name=models.CharField(verbose_name="Nombre Canónico")
    price=models.DecimalField(verbose_name="Precio",max_digits=15, decimal_places=2, default=0.00, validators=[MinValueValidator(0.00)])  
    discount=models.DecimalField(verbose_name="Descuento",max_digits=15, decimal_places=2, default=0.00, validators=[MinValueValidator(0.00),MaxValueValidator(100.00)])
    category=models.ManyToManyField(Category, verbose_name="Categoría", related_name='products', blank=True)
    about=models.TextField(verbose_name="Descripción",blank=True,null=True)
    details=models.TextField(verbose_name="Detalles",blank=True,null=True)
    main_image=models.ImageField(verbose_name="Imagen",upload_to=get_unique_filename,blank=True,null=True)
    stock=models.PositiveIntegerField(verbose_name="Stock",default=0)
    views=models.PositiveIntegerField(verbose_name="Vistas",default=0)
    purchases=models.PositiveIntegerField(verbose_name="Compras",default=0)
    available=models.BooleanField(verbose_name="Disponible",default=False)
    created_at=models.DateTimeField(auto_now_add=True,verbose_name="Fecha de Creación")

    def __str__(self):
        return self.name
    
    def get_discount_price(self):
        discount_price=self.price*(1-self.discount/100)
        return round(discount_price,2)
    
    def get_stars(self):
        reviews = self.reviews.all()
        if not reviews.exists():
            return 0.0
        avg = reviews.aggregate(models.Avg('rating'))['rating__avg']
        return round(avg or 0.0, 1)
    
    def get_is_new(self):
        return self.created_at >= timezone.now() - timezone.timedelta(days=3)
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

class ProductImage(models.Model):
    product = models.ForeignKey(Products, verbose_name="Producto", on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(verbose_name="Imagen", upload_to=get_unique_filename)

    def __str__(self):
        return f"{self.product.name} - Imagen {self.id}"
    
    class Meta:
        verbose_name = 'Imagen del Producto'
        verbose_name_plural = 'Imágenes del Producto'

class Reviews(models.Model):
    product = models.ForeignKey(Products, verbose_name="Producto", on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('app_auth.User', verbose_name="Usuario", on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(verbose_name="Calificación", validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(verbose_name="Comentario", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    def __str__(self):
        return f"Reseña de {self.user.email} para {self.product.name} - Calificación: {self.rating}"
    
    class Meta:
        verbose_name = 'Reseña'
        verbose_name_plural = 'Reseñas'
        ordering = ['-created_at']
