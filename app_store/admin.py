from django.contrib import admin, messages
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display,action
from django.urls import reverse
from django.utils.html import format_html
from unfold.contrib.filters.admin import ChoicesDropdownFilter
from django.utils.translation import gettext_lazy as _
from app_store.models import Invoices, InvoiceProducts

class InvoiceProductsInline(TabularInline):
    model = InvoiceProducts
    extra = 0
    #show_change_link = True

@admin.register(Invoices)
class InvoicesAdmin(ModelAdmin):
    list_display = ['id','display_name','email','display_status','created_at']
    #add view to download invoice file
    list_display_links = ['id', 'display_name', 'email']
    search_fields = ['id', 'email', 'first_name', 'last_name']
    search_help_text = _("Buscar Factura")
    inlines = [InvoiceProductsInline]
    list_filter = ['status']

    @display(
        description=_("Estado"),
        label={
            'pending': "warning",
            'sended': "info",
            'completed': "success",
            'canceled': "danger"
        }
    )
    def display_status(self, obj):
        return obj.status, obj.get_status_display()
    
    @display(description=_("Nombre Completo"))
    def display_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    

