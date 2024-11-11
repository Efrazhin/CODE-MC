from django.db import transaction, connection
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from .models import CustomUser, BusinessManager, Empleado

@receiver(post_migrate)
def crear_grupos(sender, app_config, **kwargs):
    def asignar_permisos():
        if app_config.name != 'miapp_CODEMC':
            return print(f'A {app_config} no le corresponde la función de asignar permisos.')

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

@receiver(post_migrate)
def trigger_descontar_stock(sender, app_config,**kwargs):
    if app_config.name != "miapp_CODEMC":
        return 
    else:
        with connection.cursor() as cursor:
            cursor.execute("""
                           SELECT COUNT(*)
                           FROM information_schema.triggers
                           WHERE trigger_name = 'update_stock_after_detalleremito_insert'
                           AND event_object_table = 'miapp_codemc_detalleremito'; """)
            
            trigger_existe = cursor.fetchone()[0] > 0

            if not trigger_existe:
                cursor.execute("""
                            CREATE TRIGGER update_stock_after_detalleremito_insert
                            AFTER INSERT ON miapp_codemc_detalleremito
                            FOR EACH ROW
                            BEGIN
                               UPDATE miapp_codemc_stock
                               SET cantidad = cantidad - NEW.cantidad
                               WHERE id_stock = (SELECT stock_id FROM miapp_codemc_producto WHERE id = NEW.producto_id);
                            END;
                               """)
            else:
                return print("Ya existe este trigger.")

@receiver(post_migrate)
def trigger_agregar_stock(sender, app_config,**kwargs):
    if app_config.name != "miapp_CODEMC":
        return 
    else:
        with connection.cursor() as cursor:
            cursor.execute("""
                           SELECT COUNT(*)
                           FROM information_schema.triggers
                           WHERE trigger_name = 'update_stock_after_detallecompra_insert'
                           AND event_object_table = 'miapp_codemc_detallecompra'; """)
            
            trigger_existe = cursor.fetchone()[0] > 0

            if not trigger_existe:
                cursor.execute("""
                            CREATE TRIGGER update_stock_after_detallecompra_insert
                            AFTER INSERT ON miapp_codemc_detallecompra
                            FOR EACH ROW
                            BEGIN
                               UPDATE miapp_codemc_stock
                               SET cantidad = cantidad - NEW.cantidad
                               WHERE id_stock = (SELECT stock_id FROM miapp_codemc_producto WHERE id = NEW.producto_id);
                            END;
                               """)
                print("Trigger creado exitosamente.")
            else:
                return print("Ya existe este trigger.")
