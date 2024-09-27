from django.db import models

class Clientes(models.Model):
    dni_cliente = models.CharField('DNI Cliente', primary_key=True)
    nombre = models.CharField('Nombre', max_length=100)
    apellido = models.CharField('Apellido', max_length=100)
    calle = models.CharField('Calle', max_length=100)
    nro_calle = models.IntegerField('Número de Calle')
    telefono = models.BigIntegerField('Teléfono')
    email = models.EmailField('Email', null=True, blank=True)
    fecha_nacimiento = models.DateField('Fecha de Nacimiento', null=True, blank=True)
    
class Provincias(models.Model):
    id_provincia = models.AutoField('ID Provincia', primary_key=True)
    nombre = models.CharField('Nombre', max_length=100)  

class Paises(models.Model):
    id_pais = models.AutoField('ID Pais', primary_key=True)
    nombre = models.CharField('Nombre', max_length=100)  

class Proveedores(models.Model):
    dni_proveedor = models.CharField('DNI Proveedor', primary_key=True)
    nombre = models.CharField('Nombre', max_length=100)
    apellido = models.CharField('Apellido', max_length=100)
    telefono = models.BigIntegerField('Teléfono')
    email = models.EmailField('Email')
    calle = models.CharField('Calle', max_length=100)
    ciudad = models.CharField('Ciudad', max_length=100)
    provincia = models.ForeignKey(Provincias, on_delete=models.CASCADE, verbose_name='Provincia')
    pais = models.ForeignKey(Paises, on_delete=models.CASCADE, verbose_name='País')
    descripcion = models.TextField('Descripción')
    web = models.URLField('Web', null=True, blank=True)
    comentarios = models.TextField('Observaciones', null=True, blank=True)
    nro_calle = models.IntegerField('Número de Calle')

class Cargos(models.Model):
    id_cargo = models.AutoField('ID Cargo', primary_key=True)
    nombre = models.CharField('Nombre', max_length=100)    

class Empleados(models.Model):
    dni_empleado = models.CharField('DNI Empleado', primary_key=True)
    nombre = models.CharField('Nombre', max_length=100)
    apellido = models.CharField('Apellido', max_length=100)
    contraseña = models.CharField('Contraseña', max_length=100)
    telefono = models.BigIntegerField('Teléfono')
    email = models.EmailField('Email')
    calle = models.CharField('Calle', max_length=100)
    nro_calle = models.IntegerField('Número de Calle')
    fecha_nacimiento = models.DateField('Fecha de Nacimiento')
    fecha_admision = models.DateField('Fecha de Admisión')
    cargo = models.ForeignKey(Cargos, on_delete=models.SET_NULL, null=True, verbose_name='Cargo')
    
class Usuario(models.Model):
    id_user = models.AutoField('ID Usuario', primary_key=True)
    alias = models.CharField('Alias', max_length=100)
    is_superuser = models.BooleanField()
    # config = models.ForeignKey('Configuracion', on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE, verbose_name='Empleado')

class Empresas(models.Model):
    cuit = models.CharField('CUIT/Razón social', max_length=50)
    nombre = models.CharField('Nombre', max_length=50)


class Almacenes(models.Model):
    id_almacen = models.IntegerField('ID Almacén', primary_key=True)
    telefono = models.BigIntegerField('Teléfono')
    provincia = models.ForeignKey(Provincias, on_delete=models.CASCADE, verbose_name='Provincia')
    ciudad = models.CharField('Ciudad', max_length=100)
    calle = models.CharField('Calle', max_length=100)
    nro_calle = models.IntegerField('Número de Calle')
    tamaño = models.DecimalField('Tamaño', max_digits=10, decimal_places=2)
    unidad_medida = models.CharField('Unidad de Medida', max_length=50)

class Sucursales(models.Model):
    id_sucursal = models.IntegerField('ID Sucursal', primary_key=True)
    telefono = models.BigIntegerField('Teléfono')
    provincia = models.ForeignKey(Provincias, on_delete=models.CASCADE, verbose_name='Provincia')
    ciudad = models.CharField('Ciudad', max_length=100)
    calle = models.CharField('Calle', max_length=100)
    nro_calle = models.IntegerField('Número de Calle')
    almacen = models.ForeignKey(Almacenes, on_delete=models.CASCADE, verbose_name='Almacén')

class Categorias(models.Model):
    id_categoria = models.AutoField('ID Categoría', primary_key=True)
    nombre = models.CharField('Nombre', max_length=100)
    descripcion = models.TextField('Descripción', null=True, blank=True)
    fecha_creacion = models.DateField('Fecha de Creación')

class Subcategorias(models.Model):
    id_subcategoria = models.AutoField('ID Subcategoría', primary_key=True)
    nombre = models.CharField('Nombre', max_length=100)
    descripcion = models.TextField('Descripción', null=True, blank=True)
    fecha_creacion = models.DateField('Fecha de Creación')
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE, verbose_name='Categoría')

class Stock(models.Model):
    id_stock = models.AutoField('ID Stock', primary_key=True)
    cantidad = models.IntegerField('Cantidad')

class Marcas(models.Model):
    id_marca = models.AutoField('ID Marca', primary_key=True)
    nombre = models.CharField('Nombre', max_length=100)

class Productos(models.Model):
    id_producto = models.AutoField('ID Producto', primary_key=True)
    nombre = models.CharField('Nombre', max_length=100)
    descripcion = models.TextField('Descripción')
    precio = models.DecimalField('Precio', max_digits=10, decimal_places=2)
    tamaño = models.DecimalField('Tamaño', max_digits=10, decimal_places=2)
    unidad_medida = models.CharField('Unidad de Medida', max_length=50, null=True, blank=True)
    marca = models.ForeignKey(Marcas, on_delete=models.CASCADE, verbose_name='Marcas')
    subcategoria = models.ForeignKey(Subcategorias, on_delete=models.CASCADE, verbose_name='Subcategorías')
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE, verbose_name='Categorías')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, verbose_name='Stock')



# class Configuraciones(models.Model):
#     id_config = models.AutoField('ID Configuración', primary_key=True)
#     tema = models.CharField('Tema', max_length=100)
#     idioma = models.CharField('Idioma', max_length=50)
#     moneda = models.ForeignKey('Moneda', on_delete=models.CASCADE)

# class Monedas(models.Model):
#     id_moneda = models.AutoField('ID Moneda', primary_key=True)
#     nombre = models.CharField('Nombre', max_length=100)

class Remitos(models.Model):
    id_remito = models.AutoField('ID Remito', primary_key=True)
    fecha = models.DateField('Fecha')
    descripcion = models.TextField('Descripción')
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, verbose_name='Cliente')
    empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE, verbose_name='Empleado')
    almacen = models.ForeignKey(Almacenes, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Almacén')
    sucursal = models.ForeignKey(Sucursales, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Sucursal')

class DetallesRemitos(models.Model):
    id_detalle_remito = models.AutoField('ID Detalle Remito', primary_key=True)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, verbose_name='Almacén')
    cantidad = models.IntegerField('Cantidad')
    descuento = models.DecimalField('Descuento', max_digits=5, decimal_places=2)
    importe = models.DecimalField('Importe', max_digits=10, decimal_places=2)
    remito = models.ForeignKey(Remitos, on_delete=models.CASCADE, verbose_name='Remito')

class Compras(models.Model):
    id_compra = models.AutoField('ID Compra', primary_key=True)
    fecha = models.DateField('Fecha')
    descripcion = models.TextField('Descripción')
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE, verbose_name='Proveedor')
    empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE, verbose_name='Empleado')

class DetallesCompras(models.Model):
    id_detalle_compra = models.AutoField('ID Detalle Compra', primary_key=True)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, verbose_name='Producto')
    cantidad = models.IntegerField('Cantidad')
    importe = models.DecimalField('Importe', max_digits=10, decimal_places=2)
    compra = models.ForeignKey(Compras, on_delete=models.CASCADE, verbose_name='Compra')
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE, verbose_name='Proveedor')

class Presupuestos(models.Model):
    id_presupuesto = models.AutoField('ID Presupuesto', primary_key=True)
    fecha = models.DateField('Fecha')
    descripcion = models.TextField('Descripción')
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, verbose_name='Clientes')
    empleado = models.ForeignKey(Empleados, on_delete=models.CASCADE, verbose_name='Empleados')
    sucursal = models.ForeignKey(Sucursales, on_delete=models.CASCADE, verbose_name='Sucursales')

class DetallePresupuesto(models.Model):
    id_detalle_presupuesto = models.AutoField('ID Detalle Presupuesto', primary_key=True)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, verbose_name='Producto')
    cantidad = models.IntegerField('Cantidad')
    descuento = models.DecimalField('Descuento', max_digits=5, decimal_places=2)
    importe = models.DecimalField('Importe', max_digits=10, decimal_places=2)
    presupuesto = models.ForeignKey(Presupuestos, on_delete=models.CASCADE, verbose_name='Presupuesto')

