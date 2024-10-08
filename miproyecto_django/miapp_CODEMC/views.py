from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate

from . import forms

# Create your views here.
def index(request):
    ctx = {}
    return render(request, 'miapp_CODEMC/service/index.html', ctx)

def planes(request):
    return render(request, "miapp_CODEMC/service/Planes.html")

def contacto(request):
    return render(request, "miapp_CODEMC/service/Contacto.html")

def inicio_gestion(request):
    return render(request, "miapp_CODEMC/home.html")

def sucursales(request):
    return render(request, "miapp_CODEMC/sucursales.html")

def estadisticas(request):
    return render(request, "miapp_CODEMC/estadisticas.html")
    
def provedores(request):
    return render(request, "miapp_CODEMC/provedores.html")

def libros(request):
    return render(request, "miapp_CODEMC/libros.html")
    
def empleados(request):
    return render(request, "miapp_CODEMC/empleados.html")
    
def depositos(request):
    return render(request, "miapp_CODEMC/depositos.html")
    
def configuracion(request):
    return render(request, "miapp_CODEMC/configuracion.html")
    
def compras(request):
    return render(request,"miapp_CODEMC/compras.html")
    
def clientes(request):
    return render(request,"miapp_CODEMC/clientes.html")

def ventas(request):
    return render(request,"miapp_CODEMC/ventas.html")

def user_login(request):
<<<<<<< HEAD
    if request.method == 'POST':
        form = forms.FormLogin(request.POST)
        if form.is_valid():
            return redirect('home')
=======
    
    if request.method == 'GET':
        ctx = {'form' : AuthenticationForm}
        return render (request, "miapp_CODEMC/login/user-login.html, ctx")
    
>>>>>>> fda03cc7fcd6813b40848158018ccb2e51d9f2fa
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password']
        )
        if user is None:
            ctx = {'form' : AuthenticationForm, 'error' : 'Usuario o contraseña incorrectos'}
            return render(request,"miapp_CODEMC/login/user-login.html",ctx)
        else:
            return redirect('home')
            
    ctx = {'form' : AuthenticationForm}       
    return render (request, "miapp_CODEMC/login/user-login.html", ctx)


def company_registration(request):
    if request.method == 'POST':
        form = forms.FormRegistroEmpresa(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registro')
    else:
        form = forms.FormRegistroEmpleado()
    ctx = {"form": form}
    return render(request, "miapp_CODEMC/registrations/company-register.html", ctx)

def user_registration(request):
    if request.method == 'POST':
        form = forms.FormRegistroEmpleado(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = forms.FormRegistroEmpleado()
    ctx = {"form": form}
    return render(request, "miapp_CODEMC/registrations/user-register.html", ctx)


