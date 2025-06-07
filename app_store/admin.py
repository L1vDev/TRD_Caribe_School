from django.contrib import admin, messages
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display,action
from django.urls import reverse
from django.utils.html import format_html
from unfold.contrib.filters.admin import MultipleChoicesDropdownFilter
from django.utils.translation import gettext_lazy as _
from app_store.models import Invoices, InvoiceProducts
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.shortcuts import redirect
from app_statistics.models import SaleStatistics

class InvoiceProductsInline(TabularInline):
    model = InvoiceProducts
    extra = 0
    can_delete=False
    readonly_fields=["product_id","product_name","product_price","product_discount","quantity"]

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Invoices)
class InvoicesAdmin(ModelAdmin):
    list_display = ['display_id','display_name','email','display_status','created_at','display_processed','pdf_link']
    list_display_links = ['display_id', 'display_name', 'email']
    exclude=["invoice_file"]
    readonly_fields=['id','processed','email','first_name','last_name','phone_number','province','municipality','address','delivery_details','delivery_price']
    actions_list=["sync_stats", "reset_stats"]
    actions_detail=["generate_pdf"]
    fieldsets = (
        (
            _("Información del cliente"),
            {
                "fields": (( "first_name", "last_name"),"email","phone_number"),
                "classes": ["tab"],
            },
        ),
        (
            _("Localización"),
            {
                "fields": (("province", "municipality"),"delivery_price","address","delivery_details"),
                "classes": ["tab"],
            },
        ),
        (
            (None),
            {
                "fields":("status",)
            }
        )
    )
    search_fields = ['id', 'email', 'first_name', 'last_name']
    search_help_text = _("Buscar Factura")
    inlines = [InvoiceProductsInline]
    list_filter = [
        ('status', MultipleChoicesDropdownFilter), 
        ]
    list_filter_submit=True

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
    
    @display(
        description=_("Estadística"),
        label={
            True: "success",
            False: "danger"
        }
    )
    def display_processed(self, obj):
        if obj.processed:
            return True, "Procesada"
        return False, "No Procesada"
    
    @display(description=_("Nombre Completo"))
    def display_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    @display(description=_("ID"))
    def display_id(self, obj):
        return str(obj.id)[:18]
    
    @action(description=_("Actualizar Estadísticas"))
    def sync_stats(self, request):
        invoices=Invoices.objects.filter(processed=False, status="completed").all()
        for invoice in invoices:
            invoice.generate_statistics()

        return redirect(
          reverse_lazy("admin:app_store_invoices_changelist")
        )
    
    @action(description=_("Reiniciar Estadísticas"))
    def reset_stats(self, request):
        invoices=Invoices.objects.filter(processed=True, status="completed").all()
        invoices.update(processed=False)
        SaleStatistics.objects.all().delete()

        return redirect(
          reverse_lazy("admin:app_store_invoices_changelist")
        )

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def save_model(self, request, obj, form, change):
        try:
            if obj.pk:
                old_obj=Invoices.objects.get(pk=obj.pk)
                super().save_model(request, obj, form, change)
                from app_auth.utils import send_invoice_email
                if old_obj.status != obj.status:
                    if obj.status=="canceled":
                        obj.cancel_invoice()
                    send_invoice_email(obj)
            else:
                super().save_model(request, obj, form, change)
        except ValidationError as e:
            messages.warning(request, e.message)
        except Exception as e:
            messages.error(request, _("Error al guardar la factura."))
            print(str(e))
    
    def pdf_link(self, obj):
        url = reverse('download-invoice', args=[obj.pk])
        return format_html(f'<a href="{url}" target="_blank">Descargar</a>')
    pdf_link.short_description="Descargar"

    @action(
        description=_("Generar Factura"),
    )
    def generate_pdf(self, request, object_id: int):
        invoice=Invoices.objects.get(pk=object_id)
        invoice.generate_pdf()
        return redirect(
            reverse_lazy("admin:app_store_invoices_changelist")
        )


