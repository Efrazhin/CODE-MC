from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm

 
class FormRegistroEmpresa(ModelForm):
    class Meta:
        model = Empresa
        fields = ('cuit', 'nombre') 

class FormRegistroUser(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')


class FormCliente(ModelForm):
    class Meta:
        model = Cliente
        fields = []