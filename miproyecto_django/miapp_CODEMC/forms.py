from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm


class FormLogin(ModelForm):
    class Meta:
        model = Empleado
        fields = ('dni_empleado', 'password')
   
class FormRegistroEmpresa(ModelForm):
    class Meta:
        model = Empresa
        fields = ('cuit', 'nombre') 

class FormRegistroEmpleado(UserCreationForm):
    # class Meta:
    #     model = Empleado
    #     fields = ('dni_empleado','username','first_name','last_name','email','telefono','password','password')
    pass
class FormCliente(ModelForm):
    class Meta:
        model = Cliente
        fields = []