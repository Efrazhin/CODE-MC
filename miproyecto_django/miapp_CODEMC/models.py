from django.db import models
from django.contrib.auth.models import AbstractUser, User


class Empresa(models.Model):
    cuit = models.CharField('CUIT', max_length=50, primary_key=True, unique=True)
    nombre = models.CharField('Razón social', max_length=100)
    telefono = models.CharField('Teléfono de contacto', max_length=50)
    email = models.EmailField('Email de contacto')
    descripcion = models.TextField('Descripción de actividades')

    def __str__(self):
        return self.nombre
    
class CustomUser(AbstractUser):
    dni = models.CharField('DNI', max_length=120,unique=True)
    telefono = models.CharField('Teléfono', max_length=120)
    MANAGER = 'manager'
    EMPLEADO = 'empleado'
    ROLE_CHOICES = [
        (MANAGER, 'Manager'),
        (EMPLEADO, 'Empleado')
    ]
    role = models.CharField('Rol', max_length=10, choices=ROLE_CHOICES, default=EMPLEADO)

class BusinessManager(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.empresa.nombre}"
    
#"related_name" se trata de un atributo que permite definir el nombre de la relación
#inversa en una relación entre modelos.

class Empleado(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    jefe = models.ForeignKey(BusinessManager, on_delete=models.CASCADE, related_name='empleados')

    def __str__(self):
        return self.user.username 
    

class Cliente(models.Model):
    dni_cliente = models.CharField('DNI', primary_key=True, max_length=120)
    nombre = models.CharField('Nombre', max_length=100)
    apellido = models.CharField('Apellido', max_length=100)
    calle = models.CharField('Calle', max_length=100, null=True,blank=True)
    nro_calle = models.IntegerField('Número de Calle',null=True,blank=True)
    telefono = models.CharField('Teléfono', max_length=50)
    email = models.EmailField('Email', null=True, blank=True)
    fecha_nacimiento = models.DateField('Fecha de Nacimiento', null=True, blank=True)
    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE)
    
class Provincia(models.Model):
    id_provincia = models.AutoField('ID Provincia', primary_key=True)
    nombre = models.CharField('Nombre', max_length=100)  
    

class Pais(models.Model):
    id_pais = models.AutoField('ID Pais', primary_key=True)
    nombre = models.CharField('Nombre', max_length=100)  
    

class Proveedor(models.Model):
    dni_proveedor = models.CharField('DNI', primary_key=True, max_length=120)
    nombre = models.CharField('Nombre', max_length=100, null=True, blank=True)
    apellido = models.CharField('Apellido', max_length=100, null=True, blank=True)
    cuit = models.CharField('Razón social', max_length=25, null=True, blank=True)
    telefono = models.CharField('Teléfono', max_length=50)
    email = models.EmailField('Email')
    calle = models.CharField('Calle', max_length=100)
    ciudad = models.CharField('Ciudad', max_length=100)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, verbose_name='Provincia')
    pais = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True,verbose_name='País')
    descripcion = models.TextField('Descripción')
    web = models.URLField('Web', null=True, blank=True)
    comentarios = models.TextField('Observaciones', null=True, blank=True)
    nro_calle = models.IntegerField('Número de Calle')
    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE)


class Almacen(models.Model):
    id_almacen = models.IntegerField('ID Almacén', primary_key=True)
    telefono = models.CharField('Teléfono', max_length=50)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, verbose_name='Provincia')
    ciudad = models.CharField('Ciudad', max_length=100)
    calle = models.CharField('Calle', max_length=100)
    nro_calle = models.IntegerField('Número de Calle')
    tamaño = models.DecimalField('Tamaño', max_digits=10, decimal_places=2)
    unidad_medida = models.CharField('Unidad de Medida', max_length=50)
    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE)

class Sucursal(models.Model):
    id_sucursal = models.IntegerField('ID Sucursal', primary_key=True)
    telefono = models.CharField('Teléfono', max_length=50)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, verbose_name='Provincia')
    ciudad = models.CharField('Ciudad', max_length=100)
    calle = models.CharField('Calle', max_length=100)
    nro_calle = models.IntegerField('Número de Calle')
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE, verbose_name='Almacén')
    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE)

class Categoria(models.Model):
    id_categoria = models.AutoField('ID Categoría', primary_key=True)
    nombre = models.CharField('Nombre', max_length=100)
    descripcion = models.TextField('Descripción', null=True, blank=True)
    fecha_creacion = models.DateField('Fecha de Creación')
    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE)

class Subcategoria(models.Model):
    id_subcategoria = models.AutoField('ID Subcategoría', primary_key=True)
    nombre = models.CharField('Nombre', max_length=100)
    descripcion = models.TextField('Descripción', null=True, blank=True)
    fecha_creacion = models.DateField('Fecha de Creación')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categoría')
   

class Stock(models.Model):
    id_stock = models.AutoField('ID Stock', primary_key=True)
    cantidad = models.IntegerField('Cantidad')


class Producto(models.Model):
    id_producto = models.AutoField('ID Producto', primary_key=True)
    nombre = models.CharField('Nombre', max_length=100)
    descripcion = models.TextField('Descripción')
    precio = models.DecimalField('Precio', max_digits=10, decimal_places=2)
    tamaño = models.DecimalField('Tamaño', max_digits=10, decimal_places=2)
    unidad_medida = models.CharField('Unidad de Medida', max_length=50, null=True, blank=True)
    fecha_vencimiento = models.DateField('Fecha de vencimiento', null=True, blank=True)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.CASCADE, verbose_name='Subcategorías')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categorías')
    stock = models.OneToOneField(Stock, on_delete=models.CASCADE, verbose_name='Stock')
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE, null=True, blank=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, null=True, blank=True)

    

# class Configuraciones(models.Model):
#     id_config = models.AutoField('ID Configuración', primary_key=True)
#     tema = models.CharField('Tema', max_length=100)
#     idioma = models.CharField('Idioma', max_length=50)
#     moneda = models.ForeignKey('Moneda', on_delete=models.CASCADE)

# class Monedas(models.Model):
#     id_moneda = models.AutoField('ID Moneda', primary_key=True)
#     nombre = models.CharField('Nombre', max_length=100)

class Remito(models.Model):
    id_remito = models.AutoField('ID Remito', primary_key=True)
    fecha = models.DateField('Fecha')
    descripcion = models.TextField('Descripción')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Cliente', null=True, blank=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, verbose_name='Empleado')
    almacen = models.ForeignKey(Almacen, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Almacén')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Sucursal')
    
    
class DetalleRemito(models.Model):
    id_detalle_remito = models.AutoField('ID Detalle Remito', primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Almacén')
    cantidad = models.IntegerField('Cantidad')
    descuento = models.DecimalField('Descuento', max_digits=5, decimal_places=2)
    importe = models.DecimalField('Importe', max_digits=10, decimal_places=2)
    remito = models.ForeignKey(Remito, on_delete=models.CASCADE, verbose_name='Remito')

class Compra(models.Model):
    id_compra = models.AutoField('ID Compra', primary_key=True)
    fecha = models.DateField('Fecha')
    descripcion = models.TextField('Descripción')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, verbose_name='Proveedor')
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, verbose_name='Empleado')
   

class DetalleCompra(models.Model):
    id_detalle_compra = models.AutoField('ID Detalle Compra', primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto')
    cantidad = models.IntegerField('Cantidad')
    importe = models.DecimalField('Importe', max_digits=10, decimal_places=2)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, verbose_name='Compra')

class Presupuesto(models.Model):
    id_presupuesto = models.AutoField('ID Presupuesto', primary_key=True)
    fecha = models.DateField('Fecha')
    descripcion = models.TextField('Descripción')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Clientes')
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, verbose_name='Empleados')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, verbose_name='Sucursales')
    
class DetallePresupuesto(models.Model):
    id_detalle_presupuesto = models.AutoField('ID Detalle Presupuesto', primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto')
    cantidad = models.IntegerField('Cantidad')
    descuento = models.DecimalField('Descuento', max_digits=5, decimal_places=2)
    importe = models.DecimalField('Importe', max_digits=10, decimal_places=2)
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE, verbose_name='Presupuesto')

