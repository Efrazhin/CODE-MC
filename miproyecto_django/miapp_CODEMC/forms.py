from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm


class FormLogin(ModelForm):
    class Meta:
        model = Empleado
        fields = ('username', 'password')
   
class FormRegistroEmpresa(ModelForm):
    class Meta:
        model = Empresa
        fields = ('cuit', 'nombre') 

class FormRegistroEmpleado(UserCreationForm):
    class Meta:
        model = Empleado
        fields = ('username','first_name','last_name','dni_empleado','telefono','email')

class FormCliente(ModelForm):
    class Meta:
        model = Cliente
        fields = []