from django.forms import *
from .models import *
from django.contrib.auth.forms import UserCreationForm
from localflavor.ar.forms import ARCUITField, ARDNIField, ARProvinceSelect, PROVINCE_CHOICES
from django_countries import countries
from django.utils import timezone


 
class FormRegistroEmpresa(ModelForm):
    class Meta:
        model = Empresa
        fields = ('cuit', 'nombre', 'telefono','email','descripcion') 

class FormRegistroUser(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'dni','first_name','last_name','email', 'telefono', 'password')
        widgets = {
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'dni': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tamaño'}),
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de calle'}),
            'email': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número de calle'}),
            'telefono': TextInput(attrs={'class': 'form-control', 'placeholder': 'Unidad de medida'}),
            'password': TextInput(attrs={'class': 'form-control', 'placeholder': 'Unidad de medida'}),
        }

class FormCliente(ModelForm):
    class Meta:
        model = Cliente
        fields = ["dni_cliente","nombre","apellido","calle","nro_calle","telefono","email","fecha_nacimiento"]

class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']  
        widgets = {
                'nombre': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
                'descripcion': Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción'}),
            }



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
            'cuit', 'nombre', 'telefono', 
            'email', 'pais','provincia', 'ciudad', 'calle', 'nro_calle',   
            'descripcion', 'web', 'comentarios'  
        ]
        widgets = {
            'cuit': NumberInput(attrs={'class': 'form-control', 'placeholder': 'CUIT'}),
            'nombre': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'telefono': TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'provincia': TextInput(attrs={'class': 'form-control', 'placeholder': 'Provincia'}),
            'ciudad': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad'}),
            'calle': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de calle'}),
            'nro_calle': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número de calle'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción'}),
            'web': TextInput(attrs={'class': 'form-control', 'placeholder': 'Página web (opcional)'}),
            'comentarios': TextInput(attrs={'class': 'form-control', 'placeholder': 'Comentarios (opcional)'}),
        }
    def __init__(self,*args, **kwargs):
        super(SucursalForm, self).__init__(*args, **kwargs)
        self.fields['pais'].widget.attrs.update(
            {'class': 'form-control', 
                'placeholder': 'Pais'})
class AlmacenForm(ModelForm):
    provincia = ChoiceField(choices=PROVINCE_CHOICES, widget=ARProvinceSelect, label='Provincia')
    class Meta:
        model = Almacen
        fields = [
            'telefono', 'provincia', 'ciudad', 
            'calle', 'nro_calle', 'tamaño', 'unidad_medida'
        ]
        widgets = {
                'telefono': TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
                'ciudad': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad'}),
                'calle': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de calle'}),
                'nro_calle': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número de calle'}),
                'tamaño': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tamaño'}),
                'unidad_medida': TextInput(attrs={'class': 'form-control', 'placeholder': 'Unidad de medida'}),

            }
    def __init__(self,*args, **kwargs):
        super(SucursalForm, self).__init__(*args, **kwargs)
        self.fields['provincia'].widget.attrs.update(
            {'class': 'form-control', 
                'placeholder': 'Provincia'})
    # Agregamo' este bloq' para q' al momento de que se guarde la selección de una provincia, lo haga 
    # con su nombre y no con su código (usamos el selector de provincias del paquete de localflavor.ar, el cual se 
    # genera a partir de una lista con tuplas de valores con cada código de provincia y el nombre correspondiente)
    def clean_provincia(self):
        provincia_code = self.cleaned_data.get('provincia')
        provincia_name = dict(PROVINCE_CHOICES).get(provincia_code)
        return provincia_name

class SucursalForm(ModelForm):
    provincia = CharField(widget=ARProvinceSelect, label='Provincia')
    class Meta:
        model = Sucursal
        fields = ['telefono', 'provincia', 'ciudad', 'calle', 'nro_calle', 'almacen']
        widgets = {
            'telefono': TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'ciudad': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad'}),
            'calle': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de calle'}),
            'nro_calle': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número de calle'}),
        }
    def __init__(self,*args, **kwargs):
        super(SucursalForm, self).__init__(*args, **kwargs)
        self.fields['almacen'].widget.attrs.update(
            {'class': 'form-control', 
                'placeholder': 'Almacén'})
        self.fields['provincia'].widget.attrs.update(
            {'class': 'form-control', 
                'placeholder': 'Provincia'})
        
    def clean_provincia(self):
        provincia_code = self.cleaned_data.get('provincia')
        provincia_name = dict(PROVINCE_CHOICES).get(provincia_code)
        return provincia_name
    
#revisar para reducir
class SeleccionUbicacion(forms.Form):
    ubicacion = ChoiceField(
        initial= [('','Selecciona tu ubicación')],
        choices = [],
        label = 'Ubicación')

    def __init__(self,*args, **kwargs):
        user = kwargs.pop('user',None)
        super(SeleccionUbicacion, self).__init__(*args, **kwargs)
        
        ubicacion_actual_obj = None

        if user:
            empresa = user.empresa
            if hasattr(user, 'ubicacion'):
                ubicacion_actual_obj = user.ubicacion
            
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
            opciones_almacenes = [(f"Almacen_{almacen.id_almacen}", f"Almacén {almacen.nombre}: {almacen.calle} {almacen.nro_calle}") for almacen in almacenes]
            opciones_sucursales = [(f"Sucursal_{sucursal.id_sucursal}", f"Sucursal {sucursal.nombre}: {sucursal.calle} {sucursal.nro_calle}") for sucursal in sucursales]

            # Establecer las opciones de elección
            self.fields['ubicacion'].choices += opciones_almacenes + opciones_sucursales


class SubcategoriaForm(ModelForm):
    class Meta:
        model = Subcategoria
        fields = ['nombre', 'descripcion', 'categoria']
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user',None)
        super(SubcategoriaForm, self).__init__(*args, **kwargs)

        if user and user.empresa:
            self.fields['categoria'].queryset = Categoria.objects.filter(empresa=user.empresa)
            self.fields['categoria'].widget.attrs.update(
                {'class': 'form-control', 
                 'placeholder': 'Categoría'}
            )


class StockForm(ModelForm):
    class Meta:
        model = Stock
        fields = ['cantidad']
        widgets = {
            'cantidad': NumberInput(attrs={'class':'form-control','placeholder':'Stock'})
        }
        

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = [ 'cod_producto',
            'nombre', 'descripcion', 'precio', 'tamaño', 
            'unidad_medida', 'fecha_vencimiento', 'categoria', 
            'subcategoria', 
        ]
        widgets = {
            'cod_producto': TextInput(attrs={'class': 'form-control', 'placeholder': 'Código de producto'}),
            'nombre': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripcion'}),
            'precio': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'tamaño': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tamaño'}),
            'unidad_medida': TextInput(attrs={'class': 'form-control', 'placeholder': 'Unidad de medida'}),
            'fecha_vencimiento': DateInput(attrs={'class': 'form-control', 'placeholder': 'Fecha de vencimiento'}),
            'categoria': TextInput(attrs={'class': 'form-control', 'placeholder': 'Categoría'}),
            'subcategoria': TextInput(attrs={'class': 'form-control', 'placeholder': 'Subcategoría'}),
        }
    

class RemitoForm(ModelForm):
    class Meta:
        model = Remito
        fields = ['orden','fecha', 'descripcion', 'cliente','iva','forma_pago']
        widgets = {
            'orden': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Orden'}),
            'fecha': DateInput(attrs={'class': 'form-control', 'placeholder': 'Fecha'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripcion'}),
            'proveedor': TextInput(attrs={'class': 'form-control', 'placeholder': 'Proveedor'}),
            'iva': NumberInput(attrs={'class': 'form-control', 'placeholder': 'IVA (%)'}),
            'forma_pago': TextInput(attrs={'class': 'form-control', 'placeholder': 'Forma de pago'}),
        }

    def __init__(self,*args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(RemitoForm, self).__init__(*args,**kwargs)

        self.fields['fecha'].initial = timezone.localtime(timezone.now()).date()
        self.fields['fecha'].widget.attrs['readonly']=True

        self.fields['orden'].widget.attrs['readonly']=True

        if hasattr(self.user, 'empresa'):
            self.fields['cliente'].queryset = Cliente.objects.filter(empresa=self.user.empresa)

        if self.instance and self.instance.pk:
            self.fields['orden'].initial = self.instance.orden  # Por si tengo q llamar un formu de modificación
        else:
            self.fields['orden'].initial = self.generar_nro_orden()

    def generar_nro_orden(self):

        hoy = timezone.localtime(timezone.now()).date()

        ubi_user = self.user.ubicacion

        ubi_nombre = ubi_user.almacen.nombre if ubi_user.almacen else ubi_user.sucursal.nombre

        ultimo_remito = Remito.objects.filter(
            fecha=hoy, ubicacion=ubi_user).order_by('-orden').first()
        
        if ultimo_remito:
            ultimo_nro = int(ultimo_remito.orden.split('-')[-1])
            new_nro = ultimo_nro + 1
        else:
            new_nro = 1

        return f"{ubi_nombre}-{new_nro:08}"



#revisar
class DetalleRemitoForm(ModelForm):
    class Meta:
        model = DetalleRemito
        fields = ['producto', 'cantidad', 'descuento',]
        widgets = {
            'cantidad': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad'}),
            'descuento': Textarea(attrs={'class': 'form-control', 'placeholder': 'Descuento'}),
        }

    def __init__(self,*args, **kwargs):
        user = kwargs.pop('user', None)
        super(DetalleRemitoForm, self).__init__(*args, **kwargs)

        ubicar = None

        if hasattr(user,'ubicacion'):
            ubicar = user.ubicacion
        
        if ubicar is not None:
            self.fields['producto'].queryset = Producto.objects.filter(ubicacion=ubicar)
            self.fields['producto'].widget.attrs.update(
                {'class': 'form-control', 
                 'placeholder': 'Producto'}
            )
        else:
            pass

        

class CompraForm(ModelForm):
    class Meta:
        model = Compra
        fields = ['orden','fecha', 'descripcion', 'proveedor', 'iva','forma_pago',]
        widgets = {
            'orden': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Orden'}),
            'fecha': DateInput(attrs={'class': 'form-control', 'placeholder': 'Fecha'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripcion'}),
            'proveedor': TextInput(attrs={'class': 'form-control', 'placeholder': 'Proveedor'}),
            'iva': NumberInput(attrs={'class': 'form-control', 'placeholder': 'IVA (%)'}),
            'forma_pago': TextInput(attrs={'class': 'form-control', 'placeholder': 'Forma de pago'}),
        }
    def __init__(self,*args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CompraForm, self).__init__(*args,**kwargs)

        self.fields['fecha'].initial = timezone.localtime(timezone.now()).date()
        self.fields['fecha'].widget.attrs['readonly']=True

        self.fields['orden'].widget.attrs['readonly']=True

        if hasattr(self.user, 'empresa'):
            self.fields['proveedor'].queryset = Proveedor.objects.filter(empresa=self.user.empresa)

        if self.instance and self.instance.pk:
            self.fields['orden'].initial = self.instance.orden  # Por si tengo q llamar un formu de modificación
        else:
            self.fields['orden'].initial = self.generar_nro_orden()

    def generar_nro_orden(self):

        hoy = timezone.localtime(timezone.now()).date()

        ubi_user = self.user.ubicacion

        ubi_nombre = ubi_user.almacen.nombre if ubi_user.almacen else ubi_user.sucursal.nombre

        ultima_compra = Compra.objects.filter(
            fecha=hoy, ubicacion=ubi_user).order_by('-orden').first()
        
        if ultima_compra:
            ultimo_nro = int(ultima_compra.orden.split('-')[-1])
            new_nro = ultimo_nro + 1
        else:
            new_nro = 1

        return f"{ubi_nombre}-{new_nro:08}"

class DetalleCompraForm(ModelForm):
    class Meta:
        model = DetalleCompra
        fields = ['producto', 'cantidad', 'descuento']
        widgets = {
            'cantidad': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad'}),
            'descuento': Textarea(attrs={'class': 'form-control', 'placeholder': 'Descuento'}),
        }
    def __init__(self,*args, **kwargs):
        user = kwargs.pop('user', None)
        super(DetalleCompraForm, self).__init__(*args, **kwargs)

        ubicar = None

        if hasattr(user,'ubicacion'):
            ubicar = user.ubicacion
        
        if ubicar is not None:
            self.fields['producto'].queryset = Producto.objects.filter(ubicacion=ubicar)
            self.fields['producto'].widget.attrs.update(
                {'class': 'form-control', 
                 'placeholder': 'Producto'}
            )
        else:
            pass


class PresupuestoForm(ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['fecha', 'descripcion', 'cliente', 'sucursal']

class DetallePresupuestoForm(ModelForm):
    class Meta:
        model = DetallePresupuesto
        fields = ['producto', 'cantidad', 'descuento', 'importe', 'presupuesto']

