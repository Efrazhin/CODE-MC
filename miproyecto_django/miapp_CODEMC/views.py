from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import CustomUser, BusinessManager, Empleado
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
    form = AuthenticationForm()
    if request.method == 'GET':
        ctx = {'form' : form}
        return render(request, "miapp_CODEMC/signin/user-login.html", ctx)
    
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            ctx = {'form' : form, 'error' : 'Usuario o contraseña incorrectos'}
            return render(request, "miapp_CODEMC/signin/user-login.html", ctx)
        else:
            login(request, user)
            return redirect('home')
                 

def user_signout(request):
    try:
        logout(request)
    except:
        pass
    return redirect('index')

def company_registration(request):
    form = forms.FormRegistroEmpresa()
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('registro')
    else:
        form_empresa = forms.FormRegistroEmpresa()
        form_user = forms.FormRegistroUser()
    ctx = {"form_empresa": form_empresa,
           "form_user": form_user}
    return render(request, "miapp_CODEMC/registrations/company-register.html", ctx)

def user_registration(request):
    if request.method == 'POST':
        form_user = forms.FormRegistroUser(request.POST)
        if request.resolver_match.url_name == 'registro-usuario':
            form_empresa = forms.FormRegistroEmpresa(request.POST)
            if form_user.is_valid() and form_empresa.is_valid():
                user = form_user.save(commit=False)
                user.role = CustomUser.MANAGER
                user.save()

                empresa = form_empresa.save()
                
                BusinessManager.objects.create(user=user, empresa=empresa)
                
                login(request, user)
                return redirect('home')
        else:
            if request.user.is_authenticated:
                if form_user.is_valid():
                    user = form_user.save()
                    try:
                        jefe = BusinessManager.objects.get(user=request.user)

                        Empleado.objects.create(user=user, jefe=jefe)

                        return redirect('home')
                    except BusinessManager.DoesNotExist:
                        return HttpResponse("Manager no existe")                
    else:
        
        form_empresa = None
        form_user = forms.FormRegistroUser()
        if request.resolver_match.url_name == 'registro-usuario':
            form_empresa = forms.FormRegistroEmpresa()

    ctx = {"form_user": form_user}        
    if form_empresa:
        ctx["form_empresa"] = form_empresa
    return render(request, "miapp_CODEMC/registrations/user-register.html", ctx)
