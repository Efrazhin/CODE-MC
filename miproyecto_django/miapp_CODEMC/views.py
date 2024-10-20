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
    return render(request, 'miapp_CODEMC/presentacion/index.html', ctx)

def planes(request):
    return render(request, "miapp_CODEMC/presentacion/Planes.html")

def contacto(request):
    return render(request, "miapp_CODEMC/presentacion/Contacto.html")

def inicio_gestion(request):
    return render(request, "miapp_CODEMC/principal/home.html")

def sucursales(request):
    return render(request, "miapp_CODEMC/principal/sucursales.html")

def estadisticas(request):
    return render(request, "miapp_CODEMC/principal/estadisticas.html")
    
def provedores(request):
    return render(request, "miapp_CODEMC/principal/provedores.html")

def libros(request):
    return render(request, "miapp_CODEMC/principal/libros.html")
    
def empleados(request):

    user_empresa = request.user.empresa
    empleado = Empleado.objects.filter(user__empresa = user_empresa)

    ctx = {"empleados" : empleado}

    return render(request, "miapp_CODEMC/principal/empleados.html", ctx)
    
def depositos(request):
    return render(request, "miapp_CODEMC/principal/depositos.html")
    
def configuracion(request):
    return render(request, "miapp_CODEMC/principal/configuracion.html")
    
def compras(request):
    return render(request,"miapp_CODEMC/principal/compras.html")
    
def clientes(request):
    return render(request,"miapp_CODEMC/principal/clientes.html")

def ventas(request):
    return render(request,"miapp_CODEMC/principal/ventas.html")

def categorias_view(request):
    # Obtenemos todas las categorías
    categorias = Categoria.objects.all()
    return render(request, 'miapp_CODEMC/principal/categorias.html', {'categorias': categorias})
def crear_categoria(request):
    if request.method == 'POST':
        form = forms.CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crear_categoria')
    else:
        form = forms.CategoriaForm()
    
    return render(request, 'miapp_CODEMC/principal/funciones/crear_categoria.html', {'form': form})
def crear_almacen(request):
    if request.method == 'POST':
        form = forms.AlmacenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crear_almacen')  # Cambia esto a la vista que deseas redirigir después de guardar
    else:
        form = forms.AlmacenForm()
    almacenes = Almacen.objects.all()
    return render(request, 'miapp_CODEMC/principal/functions/crear_almacen.html', {'form': form, 'almacenes': almacenes})
def crear_sucursal(request):
    if request.method == 'POST':
        form = forms.SucursalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crear_sucursal')  # Cambia esto a la vista que deseas redirigir después de guardar
    else:
        form = forms.SucursalForm()
    sucursales = Sucursal.objects.all()
    return render(request, 'miapp_CODEMC/principal/functions/crear_sucursal.html', {'form': form, 'sucursales': sucursales})

def eliminar_almacen(request, id_almacen):
    almacen = get_object_or_404(Almacen, id_almacen=id_almacen)
    if request.method == 'POST':
        almacen.delete()
        return redirect('crear_almacen')  # Cambia a tu vista de lista de almacenes
    return render(request, 'miapp_CODEMC/functions/eliminar_almacen.html', {'almacen': almacen})

def eliminar_sucursal(request, id_sucursal):
    sucursales = get_object_or_404(Sucursal, id_sucursal=id_sucursal)
    if request.method == 'POST':
        sucursales.delete()
        return redirect('crear_sucursal')  # Cambia a tu vista de lista de almacenes
    return render(request, 'miapp_CODEMC/functions/eliminar_sucursal.html', {'sucursal': sucursal})


def productos_por_subcategoria(request, subcategoria_id):
    # Obtenemos la subcategoría seleccionada
    subcategoria = get_object_or_404(Subcategoria, id=subcategoria_id)
    # Obtenemos los productos asociados a la subcategoría
    productos = Producto.objects.filter(subcategoria=subcategoria)
    return render(request, 'productos.html', {'subcategoria': subcategoria, 'productos': productos})

def agregar_productos(request):
    if request.method == "POST":
        form=forms.ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = forms.ProductoForm()
    return render(request, 'miapp_CODEMC/principal/productos.html', {'form': form} )

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


def user_registration(request):
    # aplicar AJAX 
    if request.method == 'POST':
        form_user = forms.FormRegistroUser(request.POST)
        if request.resolver_match.url_name == 'registro-usuario':
            
            form_empresa = forms.FormRegistroEmpresa(request.POST)
            if form_user.is_valid() and form_empresa.is_valid():
                user = form_user.save(commit=False)
                user.rol = CustomUser.MANAGER
                
                empresa = form_empresa.save()

                user.empresa = empresa

                user.save()

                BusinessManager.objects.create(user=user)
                
                login(request, user)
                return redirect('home')
        else:
            if request.user.is_authenticated:
                if form_user.is_valid():
                    user = form_user.save(commit=False)
                    user.empresa = request.user.empresa
                    user = form_user.save()
                    try:
                        jefe = BusinessManager.objects.get(user=request.user)

                        Empleado.objects.create(user=user, jefe=jefe)

                        return redirect('empleados')
                    except BusinessManager.DoesNotExist:
                        return HttpResponse("Manager no existe.")   
                else:
                    return HttpResponse("Datos no válidos")
            else:
                return HttpResponse("El administrador no está logueado; falló registro de empleado")         
    else:
        form_empresa = None
        form_user = forms.FormRegistroUser()
        if request.resolver_match.url_name == 'registro-usuario':
            form_empresa = forms.FormRegistroEmpresa()
            
    ctx = {"form_user": form_user}        
    if form_empresa:
        ctx["form_empresa"] = form_empresa
        return render(request, "miapp_CODEMC/registrations/user-register.html", ctx)
    

    return render(request,"miapp_CODEMC/principal/funciones/crear_empleado.html", ctx)

