from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser 
# Register your models here.

class CustomUserAdmin(BaseUserAdmin):
    # Define qué campos se mostrarán en la lista de usuarios
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    
    # Define qué campos se pueden buscar
    search_fields = ('email', 'first_name', 'last_name')
    
    # Define cómo se ordenarán los usuarios
    ordering = ('email',)
    
    # Configura los campos para el formulario de edición
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    # Configura los campos para el formulario de creación
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)