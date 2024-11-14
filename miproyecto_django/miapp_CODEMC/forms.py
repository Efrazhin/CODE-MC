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
        fields = ('username', 'dni','first_name','last_name','email', 'telefono','password1','password2')
        widgets = {
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'dni': NumberInput(attrs={'class': 'form-control', 'placeholder': 'DNI'}),
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'telefono': TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            
        }

    def __init__(self,*args, **kwargs):
        super(FormRegistroUser, self).__init__(*args, **kwargs)
       
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control'})
        

class FormCliente(ModelForm):
    class Meta:
        model = Cliente
        fields = ["dni_cliente","nombre","apellido","calle","nro_calle","telefono","email","fecha_nacimiento"]
        widgets = {
            'dni_cliente': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'nombre': TextInput(attrs={'class': 'form-control', 'placeholder': 'Tamaño'}),
            'apellido': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad'}),
            'calle': TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de calle'}),
            'nro_calle': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número de calle'}),
            'telefono': TextInput(attrs={'class': 'form-control', 'placeholder': 'Unidad de medida'}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder': 'Unidad de medida'}),
            'fecha_nacimiento': DateInput(attrs={'class': 'form-control', 'placeholder': 'Unidad de medida'}),
        }

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
        super(ProveedorForm, self).__init__(*args, **kwargs)
        self.fields['pais'].empty_label = "Selecciona un país"
        self.fields['pais'].widget.attrs.update(
            {'class': 'form-control'})
        

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

            }
    def __init__(self,*args, **kwargs):
        super(AlmacenForm, self).__init__(*args, **kwargs)

        self.fields['provincia'].empty_label = "Selecciona una provincia"
        self.fields['provincia'].widget.attrs.update(
            {'class': 'form-control', 
                'placeholder': 'Provincia'})
        
        self.fields['provincia'].empty_label = "Selecciona una unidad de medida del tamaño"
        self.fields['unidad_medida'].widget.attrs.update(
            {'class': 'form-control', 
                'placeholder': 'Escoge la unidad de medida del tamaño de tu almacén'})
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
        self.fields['almacen'].empty_label = "Selecciona un almacén"
        self.fields['almacen'].widget.attrs.update(
            {'class': 'form-control', 
                'placeholder': 'Almacén'})
        
        self.fields['provincia'].empty_label = "Selecciona una provincia"
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
            
            almacenes = Almacen.objects.filter(empresa=empresa)
            sucursales = Sucursal.objects.filter(empresa=empresa)

            # Generar opciones para almacenes y sucursales
            opciones_almacenes = [(f"Almacen_{almacen.id_almacen}", f"Almacén {almacen.nombre}: {almacen.calle} {almacen.nro_calle}") for almacen in almacenes]
            opciones_sucursales = [(f"Sucursal_{sucursal.id_sucursal}", f"Sucursal {sucursal.nombre}: {sucursal.calle} {sucursal.nro_calle}") for sucursal in sucursales]

            # Establecer las opciones de elección
            if ubicacion_actual_obj == None:
                self.fields['ubicacion'].empty_label = "Selecciona una ubicación"
            else:
                self.fields['ubicacion'].empty_label = ubicacion_actual_obj
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

            self.fields['categoria'].empty_label = "Selecciona una categoria"
            self.fields['categoria'].widget.attrs.update(
                {'class': 'form-control', 
                 'placeholder': 'Categoría'}
            )


class StockForm(ModelForm):
    class Meta:
        model = Stock
        fields = ['cantidad']
        widgets = {
            'cantidad': NumberInput(attrs={'class':'form-control','placeholder':'Stock del producto'})
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
            'fecha_vencimiento': DateInput(attrs={'class': 'form-control', 'placeholder': 'Fecha de vencimiento'}),
        }
    def __init__(self,*args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)

        self.fields['unidad_medida'].empty_label = "Escoge la unidad de medida"
        self.fields['unidad_medida'].widget.attrs.update(
            {'class': 'form-control'})
        
        self.fields['categoria'].empty_label = "Selecciona la categoría"
        self.fields['categoria'].widget.attrs.update(
            {'class': 'form-control', 
            'placeholder': 'Escoge la categoría'})
        
        self.fields['subcategoria'].empty_label = "Selecciona la subcategoría"
        self.fields['subcategoria'].widget.attrs.update(
            {'class': 'form-control', 
            'placeholder': 'Escoge la subcategoría'})
           

class RemitoForm(ModelForm):
    class Meta:
        model = Remito
        fields = ['orden','fecha', 'descripcion', 'cliente','iva','forma_pago']
        widgets = {
            'fecha': DateInput(attrs={'class': 'form-control', 'placeholder': 'Fecha'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripcion'}),
        }

    def __init__(self,*args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(RemitoForm, self).__init__(*args,**kwargs)

        self.fields['cliente'].empty_label = "Selecciona un cliente"
        self.fields['cliente'].widget.attrs.update(
                {'class': 'form-control', 
                 'placeholder': 'Cliente'}
            )
        self.fields['forma_pago'].widget.attrs.update(
                {'class': 'form-control', 
                 'placeholder': 'Forma de pago'}
            )
        
        self.fields['iva'].empty_label = "Selecciona el tipo de IVA"
        self.fields['iva'].widget.attrs.update(
                {'class': 'form-control', 
                 'placeholder': 'IVA (%)'}
            )
        

        self.fields['fecha'].initial = timezone.localtime(timezone.now()).date()
        self.fields['fecha'].widget.attrs['readonly']=True

        self.fields['orden'].widget.attrs['readonly']=True
        self.fields['orden'].widget.attrs.update(
                {'class': 'form-control'}
            )

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
            'descuento': TextInput(attrs={'class': 'form-control', 'placeholder': 'Descuento'}),
        }

    def __init__(self,*args, **kwargs):
        user = kwargs.pop('user', None)
        super(DetalleRemitoForm, self).__init__(*args, **kwargs)

        ubicar = None

        if hasattr(user,'ubicacion'):
            ubicar = user.ubicacion
        
        if ubicar is not None:
            self.fields['producto'].queryset = Producto.objects.filter(ubicacion=ubicar)
            self.fields['producto'].empty_label = "Selecciona un producto"
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
            'fecha': DateInput(attrs={'class': 'form-control', 'placeholder': 'Fecha'}),
            'descripcion': Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripcion'}),
        }
    def __init__(self,*args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CompraForm, self).__init__(*args,**kwargs)

        self.fields['proveedor'].empty_label = "Selecciona un proveedor"
        self.fields['proveedor'].widget.attrs.update(
                {'class': 'form-control', }
            )
        self.fields['forma_pago'].widget.attrs.update(
                {'class': 'form-control', 
                 'placeholder': 'Forma de pago'}
            )
        
        self.fields['iva'].empty_label = "Selecciona el tipo de IVA"
        self.fields['iva'].widget.attrs.update(
                {'class': 'form-control', 
                 'placeholder': 'IVA (%)'}
            )
        

        self.fields['fecha'].initial = timezone.localtime(timezone.now()).date()
        self.fields['fecha'].widget.attrs['readonly']=True

        self.fields['orden'].widget.attrs['readonly']=True
        self.fields['orden'].widget.attrs.update(
                {'class': 'form-control'}
            )

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
            'descuento': TextInput(attrs={'class': 'form-control', 'placeholder': 'Descuento'}),
        }
    def __init__(self,*args, **kwargs):
        user = kwargs.pop('user', None)
        super(DetalleCompraForm, self).__init__(*args, **kwargs)

        ubicar = None

        if hasattr(user,'ubicacion'):
            ubicar = user.ubicacion
        
        if ubicar is not None:
            self.fields['producto'].queryset = Producto.objects.filter(ubicacion=ubicar)
            self.fields['producto'].empty_label = "Selecciona un producto"
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

