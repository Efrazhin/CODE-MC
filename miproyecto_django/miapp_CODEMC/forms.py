from django import forms
from .models import *

class FormularioCurso(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length= 128)
    inscriptos = forms.IntegerField(label="Inscriptos")

class FormularioLogin(forms.ModelForm):
    class Meta:
        model = Empleados
        fields = ()
   
class FormularioRegistroEmpresa(forms.ModelForm):
    class Meta:
        model = Empresas
        fields = ['cuit', 'nombre'] 

class FormCliente(forms.Form):
    model = Clientes
    fields = []