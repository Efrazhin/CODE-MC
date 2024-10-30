from django.forms import *
from .models import *
from django.contrib.auth.forms import UserCreationForm
from localflavor.ar.forms import ARCUITField, ARDNIField, ARProvinceSelect


 
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
        fields = ['nombre', 'descripcion']  # Excluye 'fecha_creacion' porque se genera automáticamente


# class ProvinciaForm(ModelForm):
#     class Meta:
#         model = Provincia
#         fields=["nombre"]


# class PaisForm(ModelForm):
#     class Meta:
#         model = Pais
#         fields=["nombre"]

class ProveedorForm(ModelForm):
    class Meta:
        model = Proveedor
        fields = [
            'dni_proveedor', 'nombre', 'apellido', 'cuit', 'telefono', 
            'email', 'calle', 'ciudad', 'provincia', 'pais', 
            'descripcion', 'web', 'comentarios', 'nro_calle', 'empresa'
        ]

class AlmacenForm(ModelForm):
    provincia = CharField(widget=ARProvinceSelect, label='Provincia')
    class Meta:
        model = Almacen
        fields = [
            'telefono', 'provincia', 'ciudad', 
            'calle', 'nro_calle', 'tamaño', 'unidad_medida'
        ]

class SucursalForm(ModelForm):
    provincia = CharField(widget=ARProvinceSelect, label='Provincia')
    class Meta:
        model = Sucursal
        fields = ['telefono', 'provincia', 'ciudad', 'calle', 'nro_calle', 'almacen', 'empresa']


class SeleccionUbicacion(forms.Form):
    ubicacion = ChoiceField(
        choices = [],
        label = 'Ubicación')

    def __init__(self,*args, **kwargs):
        user = kwargs.pop('user',None)
        super(SeleccionUbicacion, self).__init__(*args, **kwargs)

        empresa = user.empresa

        almacenes = Almacen.objects.filter(empresa=empresa)
        sucursales = Sucursal.objects.filter(empresa=empresa)

        opciones_almacenes = [(f"Almacén_{almacen.id_almacen}", f"Almacén: {almacen.calle} {almacen.nro_calle}") for almacen in almacenes]
        opciones_sucursales = [(f"Sucursal_{sucursal.id_sucursal}", f"Sucursal: {sucursal.calle} {sucursal.nro_calle}") for sucursal in sucursales]

        self.fields['ubicacion'].choices = opciones_almacenes + opciones_sucursales


class SubcategoriaForm(ModelForm):
    class Meta:
        model = Subcategoria
        fields = ['nombre', 'descripcion', 'categoria']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user',None)
        super(SubcategoriaForm, self).__init__(*args, **kwargs)

        if user and user.empresa:
            self.fields['categoria'].queryset = Categoria.objects.filter(empresa=user.empresa)


class StockForm(ModelForm):
    class Meta:
        model = Stock
        fields = ['cantidad']

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre', 'descripcion', 'precio', 'tamaño', 
            'unidad_medida', 'fecha_vencimiento', 'categoria', 
            'subcategoria', 'stock', 'almacen', 'sucursal'
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

