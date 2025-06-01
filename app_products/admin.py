from django.contrib import admin, messages
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from django.urls import reverse_lazy
from django.shortcuts import redirect
from unfold.contrib.filters.admin import MultipleRelatedDropdownFilter
from django.utils.translation import gettext_lazy as _
from app_products.models import Products, ProductImage, Category, Reviews

class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 0

@admin.register(Products)
class ProductsAdmin(ModelAdmin):
    list_display = ['name','display_available', 'price', 'discount', 'stock']
    list_display_links = ['name']
    autocomplete_fields=["category"]
    exclude=["canon_name"]
    readonly_fields=["views","purchases"]
    search_fields = ['name', 'about','details']
    search_help_text = _("Buscar Producto")
    inlines = [ProductImageInline]
    list_filter = [('category', MultipleRelatedDropdownFilter), 'available']
    actions = ['hide_show_product']
    list_filter_submit=True
    fieldsets = (
        (
            _("Información Principal"),
            {
                "fields": ("name", "price","discount", "category","stock","available"),
                "classes": ["tab"],
            },
        ),
        (
            _("Detalles"),
            {
                "fields": ("about", "details","main_image"),
                "classes": ["tab"],
            },
        ),
        (
            _("Información Ventas"),
            {
                "fields": ("purchases","views"
                ),
                "classes": ["tab"],
            },
        ),
    )
    add_fieldsets = (
        (
            _("Información Principal"),
            {
                "fields": ("name", "price","discount", "category","stock","available"),
                "classes": ["tab"],
            },
        ),
        (
            _("Detalles"),
            {
                "fields": ("about", "details","main_image"),
                "classes": ["tab"],
            },
        ),
        (
            _("Información Ventas"),
            {
                "fields": ("purchases","views"
                ),
                "classes": ["tab"],
            },
        ),
    )
    
    @display(
        description=_("Disponible"),
        label={
            True: "success",
            False: "danger"
        }
    )
    def display_available(self, obj):
        if obj.available:
            return True, "Disponible"
        return False, "No Disponible"
    
    def hide_show_product(self, request, queryset):
        for product in queryset:
            if product.available:
                product.available=False
                messages.success(request, _(f"Se ha ocultado {product.name} correctamente."))
            else:
                if product.price>0:
                    product.avaliable=True
                    messages.success(request, _(f"Se ha publicado {product.name} correctamente."))
                else:
                    messages.error(request, _(f"No se ha podido publicar {product.name}. Revisa que el precio sea correcto"))
            product.save()
        return redirect(
            reverse_lazy("admin:app_products_products_changelist")
        )       
    hide_show_product.short_description="Mostrar/Ocultar Productos"
    
@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']
    search_fields = ['name']
    search_help_text = _("Buscar Categoría")

@admin.register(Reviews)
class ReviewsAdmin(ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    list_display_links = ['product', 'user']
    readonly_fields=['product','user','rating','comment']
    search_fields = ['product__name', 'user__email', 'comment']
    search_help_text = _("Buscar Reseña")
    list_filter = [('product', MultipleRelatedDropdownFilter), ('user', MultipleRelatedDropdownFilter)]
    list_filter_submit=True

    def has_add_permission(self, request, obj=None):
        return False
