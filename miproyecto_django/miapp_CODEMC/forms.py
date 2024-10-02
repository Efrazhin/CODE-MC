from django.forms import ModelForm
from .models import *


class FormularioLogin(ModelForm):
    class Meta:
        model = Empleados
        fields = ('email','contraseña')
   
class FormularioRegistroEmpresa(ModelForm):
    class Meta:
        model = Empresas
        fields = ['cuit', 'nombre'] 

class FormularioRegistro(ModelForm):
    class Meta:
        model= Empleados
        fields = ['dni_empleado','nombre','apellido','contraseña','telefono','email','calle','nro_calle','fecha_nacimiento']

class FormCliente(ModelForm):
    class Meta:
        model = Clientes
        fields = []