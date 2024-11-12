from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from .models import *
from . import forms

# Create your views here.
def index(request):
    user = None
    if request.user.is_authenticated:
        user = request.user
    ctx = {'user':user}
    return render(request, 'miapp_CODEMC/presentacion/index.html', ctx)

def planes(request):
    return render(request, "miapp_CODEMC/presentacion/Planes.html")

def contacto(request):
    return render(request, "miapp_CODEMC/presentacion/Contacto.html")

def home(request):

    ubicacion = None
    user = request.user


    if hasattr(user,'ubicacion') and user.ubicacion:
        ubicacion = user.ubicacion
    else:
        pass

    if ubicacion is not None: 
        ctx = {'ubicacion':ubicacion}
        return render(request, "miapp_CODEMC/principal/home.html", ctx)


    return render(request, "miapp_CODEMC/principal/home.html")

def sucursales(request):
    return render(request, "miapp_CODEMC/principal/sucursales.html")

def estadisticas(request):
    return render(request, "miapp_CODEMC/principal/estadisticas.html")

def almacenes(request):
    return render(request, "miapp_CODEMC/principal/depositos.html")

@permission_required('miapp_CODEMC.view_proveedor', raise_exception=True)
def proveedores(request):
    user = request.user
    if hasattr(request.user,'empresa'):
        empresadora = user.empresa

    proveedor = Proveedor.objects.filter(empresa=empresadora)

    ctx = {"proveedores" : proveedor}
    return render(request, "miapp_CODEMC/principal/provedores.html", ctx)


@permission_required('miapp_CODEMC.add_proveedor', raise_exception=True)
def agregar_proveedor(request):
    user = request.user
    if request.method == "POST":
        form = forms.ProveedorForm(request.POST)
        if form.is_valid():
            
            proveedor = form.save(commit=False)
            if hasattr(user,'empresa'):
                proveedor.empresa = request.user.empresa
            proveedor.save()  
            messages.success(request, '¡Tu proveedor se agregó exitosamente!')
            return redirect('proveedores')
        else:
            
            ctx = {'form':form}
            messages.error(request,"Error al agregar el proveedor.")
    else:
        form = forms.ProveedorForm()
        ctx = {'form':form}
    return render(request, "miapp_CODEMC/principal/funciones/crear_proveedor.html", ctx)

def libros(request):
    return render(request, "miapp_CODEMC/principal/libros.html")

@permission_required('miapp_CODEMC.view_empleado', raise_exception=True)
def empleados(request):
    if request.user:
        user = request.user
    if hasattr(request.user,'manager'):
        manager = user.manager
    elif hasattr(request.user, 'empleado'):
        manager = user.empleado.jefe

    empleado = Empleado.objects.filter(jefe=manager)

    ctx = {"empleados" : empleado}

    return render(request, "miapp_CODEMC/principal/empleados.html", ctx)
    

def configuracion(request):
    user= request.user
    if request.method == 'POST':
        form = forms.SeleccionUbicacion(request.POST, user=request.user)
        if form.is_valid():
            ubicacion_seleccionada = form.cleaned_data['ubicacion']

            try:
                if not ubicacion_seleccionada:
                    raise ValueError("Ubicación no seleccionada")

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

                user.ubicacion = ubicar
                user.save()
                return redirect('configuracion') 

            except ObjectDoesNotExist:
                return render(request, "miapp_CODEMC/principal/error.html", {"error": "Ubicación no encontrada"})
            except ValueError as e:
                return render(request, "miapp_CODEMC/principal/configuracion.html", {"form_ubicacion": form, "error": str(e)})
    else:
        form = forms.SeleccionUbicacion(user=request.user)

    ctx = {'form_ubicacion':form}

    return render(request, "miapp_CODEMC/principal/configuracion.html", ctx)
    

#<------------------------------ Clientes ------------------------------>    
def clientes(request):
    
    if request.user:
        user = request.user
    
    if hasattr(user,'empresa'):
        empresa=user.empresa
    else:
        raise AttributeError('qe se yo, no existe el usuario')
    
    clientes = Cliente.objects.filter(empresa=empresa)

    ctx = {'clientes':clientes}

    return render(request,"miapp_CODEMC/principal/clientes.html", ctx)

def agregar_cliente(request):
    if request.user:
        user = request.user

    if request.method == 'POST':
        form = forms.FormCliente(request.POST)
        if form.is_valid():
            try:
                cliente = form.save(commit=False)
                if hasattr(user,'empresa'):
                    cliente.empresa = request.user.empresa

                cliente = form.save()
                messages.success(request, '¡Tu cliente se agregó exitosamente!')

                return redirect('clientes')
            except:
                raise ValueError("Qe se yo")
        else:
            raise ValueError("Datos mal proporcionados")
    else:
        form = forms.FormCliente()
        ctx = {'form':form}

    return render(request,"miapp_CODEMC/principal/funciones/crear_cliente.html", ctx)





#<------------------------------ Cancelar venta/compra ------------------------------>

def cancelar_proceso_venta_compra(request):
    request.session['detalles'] = []
    
    vista_previa = request.GET.get('from')
    print(vista_previa)
    if vista_previa == 'agregar-venta':
        return redirect('agregar-venta')
    elif vista_previa == 'agregar_compra':
        return redirect('agregar_compra')
    else:
        return HttpResponse("No funcó.")
        

        
#<------------------------------ Detalles ------------------------------>

def agregar_detalle(request):
    if request.user:
        user = request.user
    print("Ta todo gut hasta acá.")
    if request.method == 'POST':
        form_detalle = forms.DetalleRemitoForm(request.POST, user=user)
        
        if form_detalle.is_valid():
            
            producto = form_detalle.cleaned_data['producto']
            cantidad = form_detalle.cleaned_data['cantidad']
            descuento = float(form_detalle.cleaned_data['descuento'])
            importe = float((((100-(descuento))/100)*float(producto.precio))*cantidad)

            detalles_temp = request.session.get('detalles', [])
            detalles_temp.append({'producto_cod':producto.cod_producto, 'producto_nombre':producto.nombre,
                                  'producto_tamaño':float(producto.tamaño), 'producto_uM':producto.unidad_medida, 
                                  'producto_precio':float(producto.precio), 
                                  'cantidad':cantidad, 'descuento':descuento,
                                  'importe':importe})
            request.session['detalles'] = detalles_temp

            return JsonResponse({'success':True, 'producto_cod':producto.cod_producto, 'producto_nombre':producto.nombre,
                                  'producto_tamaño':float(producto.tamaño), 'producto_uM':producto.unidad_medida, 
                                  'producto_precio':float(producto.precio), 
                                  'cantidad':cantidad, 'descuento':descuento,
                                  'importe':importe})
        return JsonResponse({'error':'Formulario no válido, bro'}, status=400)
    return JsonResponse({'error':'Método inesperado, bro'}, status=405) 

def obtener_detalles(request,remito_id):
    detalles = DetalleRemito.objects.filter(remito=remito_id).values('producto__nombre', 'cantidad', 'importe')
    print(f"Detalles encontrados para remito_id {remito_id}: {list(detalles)}")
    return JsonResponse({'detalles': list(detalles)})

def sacar_detalle(request,producto_cod):
    if request.method == 'POST':
        detalles_temp = request.session.get('detalles',[])
        detalles_temp = [detalle for detalle in detalles_temp if detalle['producto_cod'] != producto_cod]
        request.session['detalles'] = detalles_temp
        
        return JsonResponse({'success':True, 'producto_cod':producto_cod})
        
    return JsonResponse({'error':'El método no es el esperado, bro'}, status=405)


#<------------------------------ Compras ------------------------------>

def compras(request):
    if request.user:
        user = request.user
    
    if hasattr(user,'empresa'):
        empresa=user.empresa
    else:
        raise AttributeError('qe se yo, no existe el usuario')
    
    compras = Compra.objects.filter(empresa=empresa)

    ctx = {'compras':compras}


    return render(request,"miapp_CODEMC/principal/compras.html", ctx)

def agregar_compra(request):
    if request.user:
        user = request.user

    if request.method == 'POST':
        form_compra = forms.CompraForm(request.POST, user=request.user)
        if form_compra.is_valid():
            compra = form_compra.save(commit=False)
            compra.user = user
            compra.ubicacion = user.ubicacion
            compra.empresa = user.empresa
            compra.usuario_a_cargo = request.user
            compra = form_compra.save()

            detalles_temp = request.session.get('detalles', [])
            for detalle in detalles_temp:
                cod_producto = Producto.objects.get(cod_producto=detalle['producto_cod'], ubicacion=user.ubicacion)
                DetalleCompra.objects.create(
                    compra = compra,
                    producto = cod_producto,
                    cantidad = detalle['cantidad'],
                    descuento = detalle['descuento'],
                    importe = detalle['importe'])
                    
            request.session['detalles'] = []
            
            return redirect('compras')

    else:
        form_compra = forms.CompraForm(user=user)
        
    form_detalle = forms.DetalleCompraForm(user=user)
    detalles_temp = request.session.get('detalles',[])
    
    
    ctx = {
        'compra_form':form_compra, 
        'detalle_form':form_detalle, 
        'detalles':detalles_temp,
    }

    return render(request,"miapp_CODEMC/principal/funciones/crear_compra.html", ctx)



#<------------------------------ Ventas ------------------------------>
def ventas(request):
    if request.user:
        user = request.user
    
    if hasattr(user,'empresa'):
        empresa=user.empresa
    else:
        raise AttributeError('qe se yo, no existe el usuario')
    
    remitos = Remito.objects.filter(empresa=empresa, ubicacion=user.ubicacion)

    ctx = {'remitos':remitos}


    return render(request,"miapp_CODEMC/principal/ventas.html", ctx)

#RECORDATORIO: Crear función decoradora q' evite q' el usu' registre remito sin tener una ubicación.
def agregar_venta(request):
    if request.user:
        user = request.user

    if request.method == 'POST':
        form_remito = forms.RemitoForm(request.POST, user=request.user)
        if form_remito.is_valid():
            remito = form_remito.save(commit=False)
            remito.user = user
            remito.ubicacion = user.ubicacion
            remito.empresa = user.empresa
            remito.usuario_a_cargo = request.user
            remito = form_remito.save()

            detalles_temp = request.session.get('detalles', [])
            for detalle in detalles_temp:
                cod_producto = Producto.objects.get(cod_producto=detalle['producto_cod'], ubicacion=user.ubicacion)
                DetalleRemito.objects.create(
                    remito = remito,
                    producto = cod_producto,
                    cantidad = detalle['cantidad'],
                    descuento = detalle['descuento'],
                    importe = detalle['importe'])
                    
            request.session['detalles'] = []
            
            return redirect('ventas')

    else:
        form_remito = forms.RemitoForm(user=user)
        
    form_detalle = forms.DetalleRemitoForm(user=user)
    detalles_temp = request.session.get('detalles',[])
    
    
    ctx = {
        'remito_form':form_remito, 
        'detalle_form':form_detalle, 
        'detalles':detalles_temp,
    }

    return render(request,"miapp_CODEMC/principal/funciones/crear_venta.html", ctx)


#<------------------------------ Productos ------------------------------>
#RECORDATORIO: Crear función decoradora q' evite q' el usu' registre producto sin tener una ubicación
def agregar_productos(request):
    if request.user:
        user = request.user

    if request.method == "POST":
        producto_form = forms.ProductoForm(request.POST)
        stock_form = forms.StockForm(request.POST)
        if producto_form.is_valid() and stock_form.is_valid():
            stock = stock_form.save()
            producto = producto_form.save(commit=False)
            producto.stock = stock  
            if hasattr(user,'ubicacion') and request.user.ubicacion:
                producto.ubicacion = request.user.ubicacion
            producto.save()  
            messages.success(request, '¡Tu producto se agregó exitosamente!')
            return redirect('agregar-producto')
        else:
            messages.error(request, 'Hubo un problema al guardar el producto')
            producto_form = forms.ProductoForm()
            stock_form = forms.StockForm()
    else:
        producto_form = forms.ProductoForm()
        stock_form = forms.StockForm()
    return render(request, 'miapp_CODEMC/principal/productos.html', {'producto_form':producto_form, 'stock_form':stock_form} )

def productos_view(request):
    if request.user:
        ubi = request.user.ubicacion
    productos = Producto.objects.filter(ubicacion = ubi)  
    return render(request, 'miapp_CODEMC/principal/lista_productos.html', {'productos': productos})

def eliminar_producto(request, producto_cod):
    producto = get_object_or_404(Producto, cod_producto=producto_cod)
    producto.delete()
    messages.success(request, "Producto eliminado exitosamente.")
    return redirect('productos')

#<------------------------------ Categorias y subcategorias ------------------------------>
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
            sucursal = form.save(commit=False)
            sucursal.empresa = request.user.empresa
            sucursal = form.save()
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
                    user.rol = CustomUser.EMPLEADO
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

