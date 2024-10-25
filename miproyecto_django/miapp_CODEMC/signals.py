from django.db import transaction
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from .models import CustomUser, BusinessManager, Empleado

@receiver(post_migrate)
def crear_grupos(sender, app_config, **kwargs):
    def asignar_permisos():
        if app_config.name != 'miapp_CODEMC':
            return print('Esta aplicación no corresponde a esta función')

        if (Group.objects.filter(name='Managers').exists()) and (Group.objects.filter(name='Empleados').exists()):
            return print('Los grupos ya existen.')
        managers_group, created = Group.objects.get_or_create(name='Managers')
        empleados_group, created = Group.objects.get_or_create(name='Empleados')

        permisos_managers = [
            'add_almacen','change_almacen','delete_almacen','view_almacen',
            'change_businessmanager', 'view_businessmanager', 
            'add_categoria', 'delete_categoria', 'change_categoria', 'view_categoria',
            'add_cliente', 'delete_cliente', 'change_cliente', 'view_cliente',
            'add_compra', 'delete_compra', 'change_compra', 'view_compra',
            'add_customuser', 'delete_customuser', 'change_customuser', 'view_customuser',
            'add_detallecompra', 'delete_detallecompra', 'change_detallecompra', 'view_detallecompra',
            'add_detallepresupuesto', 'delete_detallepresupuesto', 'change_detallepresupuesto', 'view_detallepresupuesto',
            'add_detalleremito', 'delete_detalleremito', 'change_detalleremito', 'view_detalleremito',
            'add_empleado', 'delete_empleado', 'change_empleado', 'view_empleado',
            'change_empresa', 'view_empresa', 
            'add_pais', 'delete_pais', 'change_pais', 'view_pais',
            'add_permission', 'change_permission', 'delete_permission', 'view_permission',
            'add_presupuesto', 'delete_presupuesto', 'change_presupuesto', 'view_presupuesto',
            'add_producto', 'delete_producto', 'change_producto', 'view_producto',
            'add_proveedor', 'delete_proveedor', 'change_proveedor', 'view_proveedor',
            'add_provincia', 'delete_provincia', 'change_provincia', 'view_provincia',
            'add_remito', 'delete_remito', 'change_remito', 'view_remito',
            'add_stock', 'delete_stock', 'change_stock', 'view_stock',
            'add_subcategoria', 'delete_subcategoria', 'change_subcategoria', 'view_subcategoria',
            'add_sucursal', 'delete_sucursal', 'change_sucursal', 'view_sucursal',
        ]

        for permiso_codename in permisos_managers:
            try:
                permiso = Permission.objects.get(codename=permiso_codename)
                managers_group.permissions.add(permiso)
                print (permiso)
            except:
                print(f'{permiso_codename} aún no existe.')

        permisos_empleados = [
            'view_almacen',
            'view_categoria',
            'add_cliente', 'change_cliente', 'view_cliente',
            'add_compra', 'change_compra', 'view_compra',
            'add_detallecompra', 'delete_detallecompra', 'change_detallecompra', 'view_detallecompra',
            'add_detallepresupuesto', 'delete_detallepresupuesto', 'change_detallepresupuesto', 'view_detallepresupuesto',
            'add_detalleremito', 'delete_detalleremito', 'change_detalleremito', 'view_detalleremito',
            'view_empresa', 
            'view_pais',
            'add_presupuesto', 'change_presupuesto', 'view_presupuesto',
            'add_producto', 'view_producto',
            'view_proveedor',
            'view_provincia',
            'add_remito', 'change_remito', 'view_remito',
            'add_stock', 'change_stock', 'view_stock',
            'view_subcategoria',
            'view_sucursal',
        ]

        for permiso_codename in permisos_empleados:
            try:
                permiso = Permission.objects.get(codename=permiso_codename)
                empleados_group.permissions.add(permiso)
            except:
                print(f'{permiso_codename} no existe.')
                
    transaction.on_commit(asignar_permisos)


@receiver(post_save, sender=CustomUser)
def asignar_grupo(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            group, created = Group.objects.get_or_create(name='Managers')
            instance.groups.add(group)

            BusinessManager.objects.get_or_create(user=instance)

        elif instance.rol == CustomUser.MANAGER:
            group, created = Group.objects.get_or_create(name='Managers')
            instance.groups.add(group)
        else:
            group, created = Group.objects.get_or_create(name='Empleados')
            instance.groups.add(group)
    print(instance.groups)
