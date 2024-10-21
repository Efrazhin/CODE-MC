from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser 
# Register your models here.

class CustomUserAdmin(BaseUserAdmin):
    # Define qué campos se mostrarán en la lista de usuarios
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'empresa')
    list_filter = ('is_staff', 'is_active', 'empresa')
    
    # Define qué campos se pueden buscar
    search_fields = ('email', 'first_name', 'last_name', 'empresa')
    
    # Define cómo se ordenarán los usuarios
    ordering = ('email',)
    
    # Configura los campos para el formulario de edición
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'empresa')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    # Configura los campos para el formulario de creación
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'empresa', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)