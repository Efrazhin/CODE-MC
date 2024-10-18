from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm

 
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
        fields = []

class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'empresa']  # Excluye 'fecha_creacion' porque se genera automáticamente
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'empresa': 'Empresa',
        }
