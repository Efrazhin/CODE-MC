from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from . import forms

# Create your views here.
def index(request):
    ctx = {}
    return render(request, 'miapp_CODEMC/index.html', ctx)

def planes(request):
    return render(request, "miapp_CODEMC/Planes.html")

def contacto(request):
    return render(request, "miapp_CODEMC/Contacto.html")

def inicio_gestion(request):
    return render(request, "miapp_codemc/inicio_gestion.html")

def sucursales(request):
    return render(request, "miapp_codemc/sucursales.html")

def estadisticas(request):
    return render(request, "miapp_codemc/estadisticas.html")

def inicio_usuario(request):
    if request.method == 'POST':
        form = forms.FormularioLogin(request.POST)
        if form.is_valid():
            form.save()
        form = forms.FormularioLogin()
    ctx = {"form": form}
    return render(request, "miapp_CODEMC/Inicio_login.html", ctx)



def inicio_registro_empresa(request):
    if request.method == 'POST':
        form = forms.FormularioRegistroEmpresa(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registro')
    else:
        form = forms.FormularioRegistroEmpresa()
    ctx = {"form": form}
    return render(request, "miapp_CODEMC/inicio_registro_empresa.html", ctx)

def inicio_registro(request):
    if request.method == 'POST':
        form = forms.FormularioRegistro(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Codigo de mierda")
    else:
        form = forms.FormularioRegistro()
    ctx = {"form": form}
    return render(request, "miapp_CODEMC/inicio_registro.html", ctx)


