from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from .models import CustomUser, BusinessManager, Empleado

@receiver(post_migrate)
def crear_grupos(sender, **kwargs):
    managers_group, created = Group.objects.get_or_create(name='Managers')
    empleados_group, created = Group.objects.get_or_create(name='Empleados')

    permisos_managers = [
        'add_almacen', 'delete_almacen', 'change_almacen', 'view_almacen',
        'change_businessmanager', 'view_businessmanager', 
        'add_categoria', 'delete_categoria', 'change_categoria', 'view_categoria',
        'add_cliente', 'delete_cliente', 'change_cliente', 'view_cliente',
        'add_compra', 'delete_compra', 'change_compra', 'view_compra',
        'add_user', 'delete_user', 'change_user', 'view_user',
        'add_detallecompra', 'delete_detallecompra', 'change_detallecompra', 'view_detallecompra',
        'add_detallepresupuesto', 'delete_detallepresupuesto', 'change_detallepresupuesto', 'view_detallepresupuesto',
        'add_detalleremito', 'delete_detalleremito', 'change_detalleremito', 'view_detalleremito',
        'add_empleado', 'delete_empleado', 'change_empleado', 'view_empleado',
        'change_empresa', 'view_empresa', 
        'add_pais', 'delete_pais', 'change_pais', 'view_pais',
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
        permiso = Permission.objects.get(codename=permiso_codename)
        managers_group.permissions.add(permiso)

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
        permiso = Permission.objects.get(codename=permiso_codename)
        empleados_group.permissions.add(permiso)

@receiver(post_save, sender=CustomUser)
def asignar_grupo(sender, instance, created, **kwargs):
    print("Señal ejecutada para:", instance.username) 
    print(instance.groups)
    print(created)
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
