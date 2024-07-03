from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
# Create your views here.
def index(request):
    ctx = {}
    return render(request,'miapp_CODEMC/index.html',ctx)

def login_sesion(request):
    return render(request,'miapp_CODEMC/Inicio_sesion.html')

def planes(request):
    return render(request,"miapp_CODEMC/Planes.html")

def contacto(request):
    return render(request, "miapp_CODEMC/Contacto.html")

def listado_productos(request):
    cursor = connection.cursor()
    query = "SELECT id_prod, nom_prod FROM `productos` ORDER BY id_prod, nom_prod"
    cursor.execute(query)

    html = """
        <html>
        <head>
            <title>Lista de cursos</title>
        </head>
        <body>
            <table style="border: 1px solid">
                <thead>
                    <tr>
                        <th>Id_producto</th>
                        <th>Nombre_producto</th>
                    </tr>
                </thead>
                <tbody>
    """
   
    # Obtener los resultados
    for (id_prod, nom_prod) in cursor.fetchall():
        html += f"""
            <tr>
                <td>{id_prod}</td>
                <td>{nom_prod}</td>
            </tr>
        """
    
    html += """
                </tbody>
                       </table>
                </body>
          </html>
    """
    
    cursor.close()  # Cerrar el cursor
    return HttpResponse(html)