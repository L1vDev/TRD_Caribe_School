from django.contrib import admin, messages
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display,action
from unfold.contrib.filters.admin import ChoicesDropdownFilter
from django.utils.translation import gettext_lazy as _
from app_products.models import Products, ProductImage, Category, Reviews

class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 0
    #show_change_link = True

@admin.register(Products)
class ProductsAdmin(ModelAdmin):
    list_display = ['name','display_available', 'price', 'discount', 'stock']
    list_display_links = ['name']
    search_fields = ['name', 'description']
    search_help_text = _("Buscar Producto")
    inlines = [ProductImageInline]
    list_filter = [('category', ChoicesDropdownFilter), 'available']
    
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
        return False, "Disponible"
    
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
    search_fields = ['product__name', 'user__username', 'comment']
    search_help_text = _("Buscar Reseña")
    list_filter = [('product', ChoicesDropdownFilter), ('user', ChoicesDropdownFilter)]
