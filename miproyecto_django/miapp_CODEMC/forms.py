from django.forms import ModelForm
from .models import *


class FormularioLogin(ModelForm):
    class Meta:
        model = Empleado
        fields = ("dni_empleado", "password")
   
class FormularioRegistroEmpresa(ModelForm):
    class Meta:
        model = Empresa
        fields = ('cuit', 'nombre') 

class FormularioRegistro(ModelForm):
    class Meta:
        model = Empleado
        fields = ('dni_empleado','username','first_name','last_name','email','telefono','password')

class FormCliente(ModelForm):
    class Meta:
        model = Cliente
        fields = []