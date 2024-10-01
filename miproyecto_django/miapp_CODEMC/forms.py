from django.forms import ModelForm
from .models import *


class FormularioLogin(ModelForm):
    class Meta:
        model = Empleados
        fields = ()
   
class FormularioRegistroEmpresa(ModelForm):
    class Meta:
        model = Empresas
        fields = ['cuit', 'nombre'] 

class FormCliente(ModelForm):
    class Meta:
        model = Clientes
        fields = []