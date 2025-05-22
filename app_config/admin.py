from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display,action
from unfold.contrib.filters.admin import ChoicesDropdownFilter
from django.utils.translation import gettext_lazy as _
from app_config.models import Province,Municipality,ContactRequest

class MunicipalityAdmin(TabularInline):
    model = Municipality
    extra = 0

@admin.register(Province)
class ProvinceAdmin(ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']
    search_fields = ['name']
    search_help_text = _("Buscar Provincia")
    inlines = [MunicipalityAdmin]

@admin.register(ContactRequest)
class ContactRequestAdmin(ModelAdmin):
    list_display = ['display_name', 'email', 'phone_number', 'created_at','dispaly_answered']
    list_display_links = ['display_name','email']
    readonly_fields=["first_name","last_name","email","phone_number","message"]
    search_fields = ['name', 'email', 'phone_number']
    search_help_text = _("Buscar Queja o Sugerencia")
    actions = ['mark_as_read']

    @action(description=_("Marcar como atendida"))
    def mark_as_read(self, request, queryset):
        for contact in queryset:
            contact.answered = True
            contact.save()
        messages.success(request, _("Las solicitudes seleccionadas han sido marcadas como leídas."))
        return redirect(reverse_lazy('admin:app_config_contactrequest_changelist'))
    
    @display(description=_("Nombre Completo"))
    def display_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    @display(
        description=_("Atendida"),
        label={
            True: "success",
            False: "danger"
        }
    )
    def dispaly_answered(self, obj):
        if obj.answered:
            return True,"Atendida"
        return False,"No Atendida"

