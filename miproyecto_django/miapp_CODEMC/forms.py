from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm

 
class FormRegistroEmpresa(ModelForm):
    class Meta:
        model = Empresa
        fields = ('cuit', 'nombre', 'telefono','email','descripcion') 

class FormRegistroUser(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username','first_name','last_name','email', 'dni','telefono')


class FormCliente(ModelForm):
    class Meta:
        model = Cliente
        fields = ["dni_cliente","nombre","apellido","calle","nro_calle","telefono","email","fecha_nacimiento","empresa"]

class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'empresa']  # Excluye 'fecha_creacion' porque se genera automáticamente


class ProvinciaForm(ModelForm):
    class Meta:
        model = Provincia
        fields=["nombre"]


class PaisForm(ModelForm):
    class Meta:
        model = Pais
        fields=["nombre"]

class ProveedorForm(ModelForm):
    class Meta:
        model = Proveedor
        fields = [
            'dni_proveedor', 'nombre', 'apellido', 'cuit', 'telefono', 
            'email', 'calle', 'ciudad', 'provincia', 'pais', 
            'descripcion', 'web', 'comentarios', 'nro_calle', 'empresa'
        ]

class AlmacenForm(ModelForm):
    class Meta:
        model = Almacen
        fields = [
            'telefono', 'provincia', 'ciudad', 
            'calle', 'nro_calle', 'tamaño', 'unidad_medida', 'empresa'
        ]

class SucursalForm(ModelForm):
    class Meta:
        model = Sucursal
        fields = ['telefono', 'provincia', 'ciudad', 'calle', 'nro_calle', 'almacen', 'empresa']

class SubcategoriaForm(ModelForm):
    class Meta:
        model = Subcategoria
        fields = ['nombre', 'descripcion', 'categoria']
 
class StockForm(ModelForm):
    class Meta:
        model = Stock
        fields = ['cantidad']

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre', 'descripcion', 'precio', 'tamaño', 
            'unidad_medida', 'fecha_vencimiento', 'subcategoria', 
            'categoria', 'stock', 'almacen', 'sucursal'
        ]

class RemitoForm(ModelForm):
    class Meta:
        model = Remito
        fields = ['fecha', 'descripcion', 'cliente', 'empleado', 'almacen', 'sucursal']

class CompraForm(ModelForm):
    class Meta:
        model = Compra
        fields = ['fecha', 'descripcion', 'proveedor', 'empleado']

class DetalleRemitoForm(ModelForm):
    class Meta:
        model = DetalleRemito
        fields = ['producto', 'cantidad', 'descuento', 'importe', 'remito']


class DetalleCompraForm(ModelForm):
    class Meta:
        model = DetalleCompra
        fields = ['producto', 'cantidad', 'importe', 'compra']

class PresupuestoForm(ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['fecha', 'descripcion', 'cliente', 'empleado', 'sucursal']

class DetallePresupuestoForm(ModelForm):
    class Meta:
        model = DetallePresupuesto
        fields = ['producto', 'cantidad', 'descuento', 'importe', 'presupuesto']

