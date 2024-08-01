from django import forms



class FormularioCurso(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length= 128)
    inscriptos = forms.IntegerField(label="Inscriptos")

class FormularioLogin(forms.Form):
    gmail = forms.EmailField(widget=forms.EmailInput(attrs={'class':'box-form','placeholder':'Ingrese su email'}))
    contraseña= forms.CharField(widget=forms.PasswordInput(attrs={'class':'box-form','placeholder':'Ingrese su contraseña'}))
    validar_contraseña= forms.CharField(widget=forms.PasswordInput(attrs={'class':'box-form','placeholder':'Confirme su contraseña'}))


