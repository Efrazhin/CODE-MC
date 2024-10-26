from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import CustomUser, BusinessManager, Empleado, Categoria, Producto, Subcategoria, Almacen, Sucursal
from . import forms

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        print(request.user)
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

@permission_required('miapp_CODEMC.view_empleado', raise_exception=True)
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
    categorias = Categoria.objects.prefetch_related('subcategoria_set').all()
    productos = None
    subcategoria_seleccionada = None

    # Verificamos que 'subcategoria_id' exista en GET y no esté vacío
    subcategoria_id = request.GET.get('subcategoria_id')
    if subcategoria_id:
        subcategoria_seleccionada = get_object_or_404(Subcategoria, id_subcategoria=subcategoria_id)
        productos = Producto.objects.filter(subcategoria=subcategoria_seleccionada)

    context = {
        'categorias': categorias,
        'productos': productos,
        'subcategoria_seleccionada': subcategoria_seleccionada,
    }
    return render(request, 'miapp_CODEMC/principal/categorias.html', context)


def productos_view(request):
    productos = Producto.objects.all()  # Obtiene todos los productos
    return render(request, 'miapp_CODEMC/principal/lista_productos.html', {'productos': productos})

def crear_categoria(request):
    if request.method == 'POST':
        categoria_form = forms.CategoriaForm(request.POST)
        if categoria_form.is_valid():
            categoria_form.save()
            return redirect('crear_categoria')
        elif 'crear_subcategoria' in request.POST:
            subcategoria_form = forms.SubcategoriaForm(request.POST)
            if subcategoria_form.is_valid():
                subcategoria_form.save()
                return redirect('crear_categoria')
        

    else:
        categoria_form = forms.CategoriaForm()
        subcategoria_form = forms.SubcategoriaForm()
    
    return render(request, 'miapp_CODEMC/principal/funciones/crear_categoria.html', {'categoria_form': categoria_form, 'subcategoria_form': subcategoria_form})

def crear_almacen(request):
    if request.method == 'POST':
        form = forms.AlmacenForm(request.POST)
        if form.is_valid():
            almacen = form.save(commit=False)
            almacen.empresa = request.user.empresa
            almacen = form.save()
            return redirect('crear_almacen') 
    else:
        form = forms.AlmacenForm()
    almacenes = Almacen.objects.all()
    return render(request, 'miapp_CODEMC/principal/funciones/crear_almacen.html', {'form': form, 'almacenes': almacenes})

def crear_sucursal(request):
    if request.method == 'POST':
        form = forms.SucursalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crear_sucursal')  # Cambia esto a la vista que deseas redirigir después de guardar
    else:
        form = forms.SucursalForm()
    sucursales = Sucursal.objects.all()
    return render(request, 'miapp_CODEMC/principal/funciones/crear_sucursal.html', {'form': form, 'sucursales': sucursales})

def eliminar_almacen(request, id_almacen):
    almacen = get_object_or_404(Almacen, id_almacen=id_almacen)
    if request.method == 'POST':
        almacen.delete()
        return redirect('crear_almacen')  # Cambia a tu vista de lista de almacenes
    return render(request, 'miapp_CODEMC/funciones/eliminar_almacen.html', {'almacen': almacen})

def eliminar_sucursal(request, id_sucursal):
    sucursal = get_object_or_404(Sucursal, id_sucursal=id_sucursal)
    if request.method == 'POST':
        sucursal.delete()
        return redirect('crear_sucursal')  # Cambia a tu vista de lista de almacenes
    return render(request, 'miapp_CODEMC/funciones/eliminar_sucursal.html', {'sucursal': sucursal})



def agregar_productos(request):
    if request.method == "POST":
        form=forms.ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agregar-producto')
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
    # IGNORAR - recordatorio: aplicar AJAX 
    if request.method == 'POST':
        form_user = forms.FormRegistroUser(request.POST)
        if request.resolver_match.url_name == 'registro-usuario':
            
            form_empresa = forms.FormRegistroEmpresa(request.POST)
            if form_user.is_valid() and form_empresa.is_valid():
                user = form_user.save(commit=False)
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
                    user.rol = CustomUser.EMPLEADO
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

