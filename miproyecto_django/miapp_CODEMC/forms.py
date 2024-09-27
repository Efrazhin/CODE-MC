from django import forms
from .models import *


class FormularioCurso(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length= 128)
    inscriptos = forms.IntegerField(label="Inscriptos")

class FormularioLogin(forms.Form):
    gmail = forms.EmailField(label="",required=False,widget=forms.EmailInput(attrs={'class':'box-form','placeholder':'Ingrese su email'}))
    contraseña= forms.CharField(label="",required=False,widget=forms.PasswordInput(attrs={'class':'box-form','placeholder':'Ingrese su contraseña'}))
   
class FormularioRegistro(forms.Form):
    gmail = forms.EmailField(label="",required=False,widget=forms.EmailInput(attrs={'class':'box-form','placeholder':'Ingrese su email'}))
    contraseña= forms.CharField(label="",required=False,widget=forms.PasswordInput(attrs={'class':'box-form','placeholder':'Ingrese su contraseña'}))
    validar_contraseña= forms.CharField(label="",required=False,widget=forms.PasswordInput(attrs={'class':'box-form','placeholder':'Confirme su contraseña'}))

class FormCliente(forms.Form):
    model = Clientes
    fields = []