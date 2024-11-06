from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

def generar_nombre_ubicacion(empresa,tipo):
    if tipo == 'A':
        ubicaciones = empresa.almacenes.filter(nombre__startswith='A').values_list('nombre',flat=True)
    elif tipo == 'S':
        ubicaciones = empresa.sucursales.filter(nombre__startswith='S').values_list('nombre',flat=True)
    else:
        pass

    nros_ubicaciones = [int(nombre[1:]) for nombre in ubicaciones]

    new_nro = 1

    while new_nro in nros_ubicaciones:
        new_nro+=1
    
    return f"{tipo}{new_nro:03}"



class Empresa(models.Model):
    cuit = models.CharField('CUIT', max_length=50, unique=True)
    nombre = models.CharField('Razón social', max_length=100, null=True)
    telefono = models.CharField('Teléfono de contacto', max_length=50, null=True)
    email = models.EmailField('Email de contacto', null=True)
    descripcion = models.TextField('Descripción de actividades', null=True)

    def __str__(self):
        return self.nombre
    

    
#"related_name" se trata de un atributo que permite definir el nombre de la relación
#inversa en una relación entre modelos.



class Almacen(models.Model):
    id_almacen = models.AutoField('id_almacen', primary_key=True)
    nombre = models.CharField('Nombre', max_length=50)
    telefono = models.CharField('Teléfono', max_length=50)
    provincia = models.CharField('Provincia', max_length=100)
    ciudad = models.CharField('Ciudad', max_length=100)
    calle = models.CharField('Calle', max_length=100)
    nro_calle = models.IntegerField('Número de Calle')
    tamaño = models.DecimalField('Tamaño', max_digits=10, decimal_places=2)

    metro_cuadrado = 'Metros cuadrados'
    MEDIDAS = [
        (metro_cuadrado,'m²'),
        ('Decámetros cuadrados','dam²'),
        ('Hectómetros cuadrados','hm²'),
    ]
    unidad_medida = models.CharField('Unidad de medida', max_length=30, choices=MEDIDAS, default=metro_cuadrado)

    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE, related_name='almacenes')

    def __str__(self):
        return f"Almacén Nº{self.id_almacen} - {self.calle} {self.nro_calle}"

    def save(self, *args, **kwargs):
        tipo = 'A'
        if not self.nombre:
            self.nombre = generar_nombre_ubicacion(self.empresa, tipo)
        super().save(*args, **kwargs)

class Sucursal(models.Model):
    id_sucursal = models.AutoField('ID Sucursal', primary_key=True)
    nombre = models.CharField('Nombre', max_length=50)
    telefono = models.CharField('Teléfono', max_length=50)
    provincia = models.CharField('Provincia', max_length=50)
    ciudad = models.CharField('Ciudad', max_length=100)
    calle = models.CharField('Calle', max_length=100)
    nro_calle = models.IntegerField('Número de Calle')
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE, verbose_name='Almacén')
    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE, related_name='sucursales')

    def __str__(self):
        return f"Sucursal Nº{self.id_sucursal} - {self.calle} {self.nro_calle}"
    
    def save(self, *args, **kwargs):
        tipo = 'S'
        if not self.nombre:
            self.nombre = generar_nombre_ubicacion(self.empresa, tipo)
        super().save(*args, **kwargs)
    
class Ubicacion(models.Model):
    SUCURSAL = 'Sucursal'
    ALMACEN = 'Almacen'
    tipo = models.CharField(max_length=20)  # "almacen" o "sucursal"
    almacen = models.ForeignKey(Almacen, null=True, blank=True, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, null=True, blank=True, on_delete=models.CASCADE)
    

class CustomUser(AbstractUser):
    dni = models.CharField('DNI', max_length=120,unique=True,null=True)
    telefono = models.CharField('Teléfono', max_length=120)
    MANAGER = 'manager'
    EMPLEADO = 'empleado'
    rol = models.CharField('Rol', max_length=10, default=MANAGER, null=True)
    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE, related_name='usuarios')
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE, max_length=100, null=True)

    
class BusinessManager(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='manager')
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}, {self.user.rol}"

class Empleado(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='empleado')
    jefe = models.ForeignKey(BusinessManager, on_delete=models.CASCADE, related_name='empleado')
    

    def __str__(self):
        return f"{self.user.username} - Empleado de {self.jefe.user.first_name} {self.jefe.user.last_name}"    
    
class Cliente(models.Model):
    dni_cliente = models.CharField('DNI', max_length=120)
    nombre = models.CharField('Nombre', max_length=100)
    apellido = models.CharField('Apellido', max_length=100)
    calle = models.CharField('Calle', max_length=100, null=True,blank=True)
    nro_calle = models.IntegerField('Número de Calle',null=True,blank=True)
    telefono = models.CharField('Teléfono', max_length=50, null=True,blank=True)
    email = models.EmailField('Email', null=True, blank=True)
    fecha_nacimiento = models.DateField('Fecha de Nacimiento', null=True, blank=True)
    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE, related_name='clientes')
    def __str__(self):
        return f"{self.dni_cliente}, {self.nombre} {self.apellido}"  
    
    
class Provincia(models.Model):
    id_provincia = models.AutoField('ID Provincia', primary_key=True)
    nombre = models.CharField('Nombre', max_length=100)  
    

class Pais(models.Model):
    id_pais = models.AutoField('ID Pais', primary_key=True)
    nombre = models.CharField('Nombre', max_length=100)  
    

class Proveedor(models.Model):
    cuit = models.CharField('CUIT', max_length=25, null=True, blank=True)
    nombre = models.CharField('Razón social/Nombre', max_length=100)
    telefono = models.CharField('Teléfono', max_length=50)
    email = models.EmailField('Email')
    pais = CountryField('País de residencia')
    provincia = models.CharField('Provincia', max_length=100)
    ciudad = models.CharField('Ciudad', max_length=100)
    calle = models.CharField('Calle', max_length=100)
    nro_calle = models.IntegerField('Número de Calle')
    descripcion = models.TextField('Descripción')
    web = models.URLField('Web (opcional)', null=True, blank=True)
    comentarios = models.TextField('Observaciones (opcional)', null=True, blank=True)
    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE, related_name='proveedores')


class Categoria(models.Model):
    id_categoria = models.AutoField('ID Categoría', primary_key=True)
    nombre = models.CharField('Nombre', max_length=100)
    descripcion = models.TextField('Descripción', null=True, blank=True)
    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nombre)

class Subcategoria(models.Model):
    id_subcategoria = models.AutoField('ID Subcategoría', primary_key=True)
    nombre = models.CharField('Nombre', max_length=100)
    descripcion = models.TextField('Descripción', null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categoría')
   
    def __str__(self):
        return str(self.nombre)

class Stock(models.Model):
    id_stock = models.AutoField('ID Stock', primary_key=True)
    cantidad = models.IntegerField('Cantidad')
    def __str__(self):
        return f'Número: {self.id_stock}'  


 
class Producto(models.Model):
    id_producto = models.AutoField('ID Producto', primary_key=True)
    nombre = models.CharField('Nombre', max_length=100)
    descripcion = models.TextField('Descripción')
    precio = models.DecimalField('Precio', max_digits=10, decimal_places=2, default=0.00)
    tamaño = models.DecimalField('Tamaño', max_digits=10, decimal_places=2)

    
    MEDIDAS = [
        ('Litros','L'),
        ('Milílitros','ml'),
        ('Centímetros cúbicos','cm³ - cc'),
        ('Kilogramos','kg'),
        ('Gramos','g'),
        ('Centímetros cúbicos','cm³ - cc'),
        ('Talla XS','Talla XS'),
        ('Talla S','Talla S'),
        ('Talla M','Talla M'),
        ('Talla L','Talla L'),
        ('Talla XL','Talla XL'),
    ]

    unidad_medida = models.CharField('Unidad de medida', max_length=30, choices=MEDIDAS, null=True)

    fecha_vencimiento = models.DateField('Fecha de vencimiento', null=True, blank=True)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.CASCADE, verbose_name='Subcategorías')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categorías')
    stock = models.OneToOneField(Stock, on_delete=models.CASCADE, verbose_name='Stock')
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE, max_length=100, null=True)



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
    orden =  models.CharField('Número de remito', max_length=30)
    fecha = models.DateField('Fecha')
    descripcion = models.TextField('Descripción')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Cliente', null=True, blank=True)
    usuario_a_cargo = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Usuario a cargo', null=True)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE, max_length=100, null=True)
    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE, null=True)

    def __str__(self):
        if self.ubicacion.almacen:
            return f"{self.ubicacion.almacen.nombre} {self.orden} - {self.fecha}" 
        elif self.ubicacion.sucursal:
            return f"{self.ubicacion.sucursal.nombre} {self.orden} - {self.fecha}" 
    
class DetalleRemito(models.Model):
    id_detalle_remito = models.AutoField('ID Detalle Remito', primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Almacén')
    cantidad = models.IntegerField('Cantidad')
    descuento = models.DecimalField('Descuento (porcentaje)', max_digits=5, decimal_places=2, default=1.00, blank=True)
    importe = models.DecimalField('Importe', max_digits=10, decimal_places=2)
    remito = models.ForeignKey(Remito, on_delete=models.CASCADE, verbose_name='Remito')

class Compra(models.Model):
    id_compra = models.AutoField('ID Compra', primary_key=True)
    fecha = models.DateField('Fecha')
    descripcion = models.TextField('Descripción')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, verbose_name='Proveedor')
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, verbose_name='Empleado')
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE, max_length=100, null=True)
    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE, null=True)

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
    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE, null=True)
    
class DetallePresupuesto(models.Model):
    id_detalle_presupuesto = models.AutoField('ID Detalle Presupuesto', primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto')
    cantidad = models.IntegerField('Cantidad')
    descuento = models.DecimalField('Descuento', max_digits=5, decimal_places=2)
    importe = models.DecimalField('Importe', max_digits=10, decimal_places=2)
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE, verbose_name='Presupuesto')

