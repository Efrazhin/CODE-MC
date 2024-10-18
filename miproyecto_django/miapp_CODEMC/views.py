from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import CustomUser, BusinessManager, Empleado, Categoria, Producto, Subcategoria
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
    return render(request, "miapp_CODEMC/empleado.html")

def crear_empleado(request):
    return render(request,"miapp_CODEMC/crear_empleado.html")
    
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

def categorias_view(request):
    # Obtenemos todas las categorías
    categorias = Categoria.objects.all()
    return render(request, 'miapp_CODEMC/categorias.html', {'categorias': categorias})
def crear_categoria(request):
    if request.method == 'POST':
        form = forms.CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = forms.CategoriaForm()
    
    return render(request, 'miapp_CODEMC/crear_categoria.html', {'form': form})


def productos_por_subcategoria(request, subcategoria_id):
    # Obtenemos la subcategoría seleccionada
    subcategoria = get_object_or_404(Subcategoria, id=subcategoria_id)
    # Obtenemos los productos asociados a la subcategoría
    productos = Producto.objects.filter(subcategoria=subcategoria)
    return render(request, 'productos.html', {'subcategoria': subcategoria, 'productos': productos})

def user_login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        ctx = {'form' : form}
        return render(request, "miapp_CODEMC/signin/user-login.html", ctx)
    
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            form = AuthenticationForm()
            ctx = {'form' : form, 'error' : 'Usuario o contraseña incorrectos'}
            return render(request, "miapp_CODEMC/signin/user-login.html", ctx)
        else:
            login(request, user)
            try:
                if hasattr(request.user,'manager'):
                    print(request.user.manager)
                elif hasattr(request.user, 'empleado'):
                    print(request.user.empleado)
            except ObjectDoesNotExist:
                messages.error(request,'El usuario no está asociado a ningún empleado o manager.')
                

            return redirect('home')
                 

def user_signout(request):
    try:
        logout(request)
    except:
        pass
    return redirect('index')

def company_registration(request):


    if request.method == 'POST':
        form = forms.FormRegistroEmpresa(request.POST)
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
                user.rol = CustomUser.MANAGER
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
