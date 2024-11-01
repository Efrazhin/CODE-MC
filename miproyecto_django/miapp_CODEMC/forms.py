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
        initial= [('','Selecciona tu ubicación')],
        choices = [],
        label = 'Ubicación')

    def __init__(self,*args, **kwargs):
        user = kwargs.pop('user',None)
        super(SeleccionUbicacion, self).__init__(*args, **kwargs)
        
        ubicacion_actual = [('','Selecciona tu ubicación')]
        ubicacion_actual_obj = None

        if user:
            empresa = user.empresa
            if hasattr(user, 'manager'):
                if hasattr(user.manager, 'ubicacion') and user.manager.ubicacion:
                    ubicacion_actual_obj = user.manager.ubicacion
                else:
                    pass
            elif hasattr(user, 'empleado'):
                if hasattr(user.empleado, 'ubicacion') and user.empleado.ubicacion:
                    ubicacion_actual_obj = user.empleado.ubicacion
                else:
                    pass
            
            # Si hay una ubicación registrada, se procede a obtener almacenes y sucursales
            if ubicacion_actual_obj:
                if ubicacion_actual_obj.tipo == 'Almacen':
                    almacenes = Almacen.objects.filter(empresa=empresa).exclude(id_almacen=ubicacion_actual_obj.almacen.id_almacen)
                    sucursales = Sucursal.objects.filter(empresa=empresa)
                elif ubicacion_actual_obj.tipo == 'Sucursal':
                    almacenes = Almacen.objects.filter(empresa=empresa)
                    sucursales = Sucursal.objects.filter(empresa=empresa).exclude(id_sucursal=ubicacion_actual_obj.sucursal.id_sucursal)
            else:
                almacenes = Almacen.objects.filter(empresa=empresa)
                sucursales = Sucursal.objects.filter(empresa=empresa)

            # Generar opciones para almacenes y sucursales
            opciones_almacenes = [(f"Almacen_{almacen.id_almacen}", f"Almacén: {almacen.calle} {almacen.nro_calle}") for almacen in almacenes]
            opciones_sucursales = [(f"Sucursal_{sucursal.id_sucursal}", f"Sucursal: {sucursal.calle} {sucursal.nro_calle}") for sucursal in sucursales]

            # Establecer las opciones de elección
            self.fields['ubicacion'].choices += opciones_almacenes + opciones_sucursales


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
            'subcategoria', 
            # 'almacen', 'sucursal'
        ]

class RemitoForm(ModelForm):
    class Meta:
        model = Remito
        fields = ['fecha', 'descripcion', 'cliente', 'empleado', 'almacen', 'sucursal']

class DetalleRemitoForm(ModelForm):
    class Meta:
        model = DetalleRemito
        fields = ['producto', 'cantidad', 'descuento', 'importe', 'remito']

    def __init__(self,*args, **kwargs):
        user = kwargs.pop('user', None)
        super(DetalleRemito, self).__init__(*args, **kwargs)

        ubicar = None

        if hasattr(user,'manager') and user.manager.ubicacion:
            ubicar = user.manager.ubicacion
        elif hasattr(user,'empleado') and user.empleado.ubicacion:
            ubicar = user.empleado.ubicacion
        else: 
            pass
        
        if ubicar is not None:
            self.fields['productos'].queryset = Producto.objects.filter(ubicacion=ubicar)
        else:
            pass

class CompraForm(ModelForm):
    class Meta:
        model = Compra
        fields = ['fecha', 'descripcion', 'proveedor', 'empleado']

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

