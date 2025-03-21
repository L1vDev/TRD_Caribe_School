from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from unfold.admin import ModelAdmin, TabularInline
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.decorators import display,action
from unfold.contrib.filters.admin import ChoicesDropdownFilter
from django.utils.translation import gettext_lazy as _
from app_auth.models import User, Worker
from django.contrib.auth.models import Group

admin.site.unregister(Group)

@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_display = ['name']
    list_display_links = ["name"]
    search_fields = ['name']
    search_help_text=_("Buscar Grupo")

@admin.register(User)
class UsersAdmin(UserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ['email',"display_full_name","dni_number","display_is_email_verified","created_at"]
    list_display_links = ["email"]
    readonly_fields=["is_email_verified"]
    search_fields = ['email','first_name','last_name','dni_number']
    ordering=["email"]
    fieldsets = (
        (
            _("Información personal"),
            {
                "fields": ("email", "password",( "first_name", "last_name"), "dni_number","phone_number","address"),
                "classes": ["tab"],
            },
        ),
        (
            _("Permisos"),
            {
                "fields": ("is_active","is_staff","is_superuser","groups","user_permissions",
                ),
                "classes": ["tab"],
            },
        ),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
        (_("Información Personal"),{
            "classes": ["tab"],
            "fields":(("first_name", "last_name"),"dni_number","address","phone_number","is_staff","is_superuser"),
        })
    )
    filter_horizontal = ('groups', 'user_permissions')
    search_help_text=_("Buscar Usuario")
    actions=["user_verify_action"]
    actions_detail=["user_verify_detail"]

    def user_verify_action(self, request, queryset):
        queryset.update(is_email_verified=True)

    @action(
        description=_("Verificar Email"),
    )
    def user_verify_detail(self,request, object_id:int):
        obj=User.objects.get(pk=object_id)
        obj.is_email_verified=True
        obj.save()
        return redirect(reverse_lazy("admin:app_auth_user_changelist"))
    user_verify_action.short_description="Verificar Email/s"
    
    @display(
        description=_("Email Verificado"),
        label={
            False: "danger",  # red
            True: "success",  # green
        },
    )
    def display_is_email_verified(self, obj):
        if obj.is_email_verified:
            return True,_("Verificado")
        return False,_("Sin Verificar")
    
    @display(
        description=_("Nombre"),
    )
    def display_full_name(self, obj):
        return obj.get_full_name()
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_staff=False)
    

@admin.register(Worker)
class WorkerAdmin(UserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ['email',"display_full_name","dni_number","display_is_email_verified","created_at","display_superuser"]
    list_display_links = ["email"]
    readonly_fields=["is_email_verified"]
    search_fields = ['email','first_name','last_name','dni_number']
    fieldsets = (
        (
            _("Información personal"),
            {
                "fields": ("email", "password",( "first_name", "last_name"), "dni_number","phone_number","address"),
                "classes": ["tab"],
            },
        ),
        (
            _("Permisos"),
            {
                "fields": ("is_active","is_staff","is_superuser","groups","user_permissions",
                ),
                "classes": ["tab"],
            },
        ),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
        (_("Información Personal"),{
            "classes": ["tab"],
            "fields":(("first_name", "last_name"),"dni_number","address","phone_number","is_staff","is_superuser"),
        })
    )
    filter_horizontal = ('groups', 'user_permissions')
    search_help_text=_("Buscar Usuario")
    actions=["user_verify_action"]
    actions_detail=["user_verify_detail"]
    ordering=["email"]

    def user_verify_action(self, request, queryset):
        queryset.update(is_email_verified=True)

    @action(
        description=_("Verificar Email"),
    )
    def user_verify_detail(self,request, object_id:int):
        obj=User.objects.get(pk=object_id)
        obj.is_email_verified=True
        obj.save()
        return redirect(
            reverse_lazy("admin:app_auth_user_changelist")
        )
    user_verify_action.short_description="Verificar Email/s"
    
    @display(
        description=_("Es Staff"),
        label={
            False: "danger",  # red
            True: "success",  # green
        },
    )
    def display_staff(self, obj):
        if obj.is_staff:
            return obj.is_staff,_("Es Staff")
        return obj.is_staff,_("No es Staff")
    
    @display(
        description=_("Email Verificado"),
        label={
            False: "danger",  # red
            True: "success",  # green
        },
    )
    def display_is_email_verified(self, obj):
        if obj.is_email_verified:
            return True,_("Verificado")
        return False,_("Sin Verificar")
    
    @display(
        description=_("Nombre"),
    )
    def display_full_name(self, obj):
        return obj.get_full_name()
    
    @display(
        description=_("Es Admin"),
        label={
            False: "danger",  # red
            True: "success",  # green
        },
    )
    def display_superuser(self, obj):
        if obj.is_superuser:
            return obj.is_superuser,_("Es Admin")
        return obj.is_superuser,_("No es Admin")
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_staff=True)