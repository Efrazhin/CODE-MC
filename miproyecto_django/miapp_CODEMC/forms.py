from django import forms

class FormularioCurso(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length= 128)
    inscriptos = forms.IntegerField(label="Inscriptos")