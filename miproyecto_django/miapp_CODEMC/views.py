from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from .models import CustomUser, BusinessManager, Empleado, Categoria, Producto, Subcategoria, Almacen, Sucursal, Ubicacion
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

def home(request):

    if request.user.manager:
        ubicacion = request.user.manager.ubicacion
    elif request.usuario.empleado:
        ubicacion = request.user.empleado.ubicacion

    if ubicacion is not None: 
        ctx = {'ubicacion':ubicacion}
        return render(request, "miapp_CODEMC/principal/home.html", ctx)


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
    if request.user.rol == 'manager':
        perfil = request.user.manager
    elif request.user.rol == 'empleado':
        perfil = request.user.empleado

    if request.method == 'POST':
        form = forms.SeleccionUbicacion(request.POST, user=request.user)
        if form.is_valid():
            ubicacion_seleccionada = form.cleaned_data['ubicacion']

            try:
                # Validar que la ubicación seleccionada tenga el formato correcto
                if not ubicacion_seleccionada:
                    raise ValueError("Ubicación no seleccionada")

                # Obtenemos el objeto de la ubicación seleccionada
                id_ubicacion = ubicacion_seleccionada.split('_')[1]
                if ubicacion_seleccionada.startswith('Almacen'):
                    almacen = Almacen.objects.get(id_almacen=id_ubicacion)
                    ubicar = Ubicacion.objects.filter(tipo=Ubicacion.ALMACEN, almacen=almacen).first()
                    if not ubicar:
                        ubicar = Ubicacion.objects.create(tipo=Ubicacion.ALMACEN, almacen=almacen)
                elif ubicacion_seleccionada.startswith('Sucursal'):
                    sucursal = Sucursal.objects.get(id_sucursal=id_ubicacion)
                    ubicar = Ubicacion.objects.filter(tipo=Ubicacion.SUCURSAL, sucursal=sucursal).first()
                    if not ubicar:
                        ubicar = Ubicacion.objects.create(tipo=Ubicacion.SUCURSAL, sucursal=sucursal)

                perfil.ubicacion = ubicar
                perfil.save()
                return redirect('configuracion')  # Redirige después de guardar

            except ObjectDoesNotExist:
                return render(request, "miapp_CODEMC/principal/error.html", {"error": "Ubicación no encontrada"})
            except ValueError as e:
                return render(request, "miapp_CODEMC/principal/configuracion.html", {"form_ubicacion": form, "error": str(e)})
    else:
        form = forms.SeleccionUbicacion(user=request.user)

    ctx = {'form_ubicacion':form}

    return render(request, "miapp_CODEMC/principal/configuracion.html", ctx)
    
def compras(request):
    return render(request,"miapp_CODEMC/principal/compras.html")
    
def clientes(request):
    return render(request,"miapp_CODEMC/principal/clientes.html")

def ventas(request):
    return render(request,"miapp_CODEMC/principal/ventas.html")


#<------------------------------Productos------------------------------>
def agregar_productos(request):
    if request.method == "POST":
        producto_form = forms.ProductoForm(request.POST)
        stock_form = forms.StockForm(request.POST)
        if producto_form.is_valid() and stock_form.is_valid():
            stock = stock_form.save()
            producto = producto_form.save(commit=False)
            producto.stock = stock  
            producto.save()  
            messages.success(request, '¡Tu producto se agregó exitosamente!')
            return redirect('agregar-producto')
    else:
        producto_form = forms.ProductoForm()
        stock_form = forms.StockForm()
    return render(request, 'miapp_CODEMC/principal/productos.html', {'producto_form':producto_form, 'stock_form':stock_form} )

def productos_view(request):
    productos = Producto.objects.all()  
    return render(request, 'miapp_CODEMC/principal/lista_productos.html', {'productos': productos})

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)
    producto.delete()
    messages.success(request, "Producto eliminado exitosamente.")
    return redirect('productos')

#<------------------------------Categorias------------------------------>
def crear_categoria(request):
    if request.method == 'POST':
        categoria_form = forms.CategoriaForm(request.POST)
        if 'crear_categoria' in request.POST:
            categoria = categoria_form.save(commit=False)
            categoria.empresa = request.user.empresa
            categoria = categoria_form.save()
            return redirect('crear_categoria')
        elif 'crear_subcategoria' in request.POST:
            subcategoria_form = forms.SubcategoriaForm(request.POST, user=request.user)
            if subcategoria_form.is_valid():
                subcategoria_form.save()
                return redirect('crear_categoria')
        

    else:
        categoria_form = forms.CategoriaForm()
        subcategoria_form = forms.SubcategoriaForm(user=request.user)
    
    return render(request, 'miapp_CODEMC/principal/funciones/crear_categoria.html', {'categoria_form': categoria_form, 'subcategoria_form': subcategoria_form})

def categorias_subcategorias_productos(request):
    categorias = Categoria.objects.prefetch_related(
        'subcategoria_set__producto_set'
    ).all()

    return render(request, 'miapp_CODEMC/principal/categorias.html', {
        'categorias': categorias
    })
#<------------------------------Almacenes------------------------------>
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
    almacenes = Almacen.objects.filter(empresa=request.user.empresa)
    return render(request, 'miapp_CODEMC/principal/funciones/crear_almacen.html', {'form': form, 'almacenes': almacenes})

def eliminar_almacen(request, id_almacen):
    almacen = get_object_or_404(Almacen, id_almacen=id_almacen)
    if request.method == 'POST':
        almacen.delete()
        return redirect('crear_almacen')  # Cambia a tu vista de lista de almacenes
    return render(request, 'miapp_CODEMC/funciones/eliminar_almacen.html', {'almacen': almacen})

#<------------------------------Sucursales------------------------------>
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



def eliminar_sucursal(request, id_sucursal):
    sucursal = get_object_or_404(Sucursal, id_sucursal=id_sucursal)
    if request.method == 'POST':
        sucursal.delete()
        return redirect('crear_sucursal')  # Cambia a tu vista de lista de almacenes
    return render(request, 'miapp_CODEMC/funciones/eliminar_sucursal.html', {'sucursal': sucursal})



#<------------------------------Inicio de sesion y Registro------------------------------>

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

