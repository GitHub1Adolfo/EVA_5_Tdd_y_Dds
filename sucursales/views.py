from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Sucursal
from django.core.exceptions import PermissionDenied

@login_required
def lista_sucursales(request):
    if request.user.rol != 'administrador':
        raise PermissionDenied
    sucursales = Sucursal.objects.all()
    return render(request, 'sucursales/lista_sucursales.html', {'sucursales': sucursales})


@login_required
def agregar_sucursal(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        Sucursal.objects.create(nombre=nombre, direccion=direccion, telefono=telefono)
        return redirect('lista_sucursales')
    return render(request, 'sucursales/agregar.html')

@login_required
def editar_sucursal(request, id):
    sucursal = get_object_or_404(Sucursal, id=id)
    if request.method == 'POST':
        sucursal.nombre = request.POST['nombre']
        sucursal.direccion = request.POST['direccion']
        sucursal.telefono = request.POST['telefono']
        sucursal.save()
        return redirect('lista_sucursales')
    return render(request, 'sucursales/editar.html', {'sucursal': sucursal})

@login_required
def eliminar_sucursal(request, id):
    sucursal = get_object_or_404(Sucursal, id=id)
    sucursal.delete()
    return redirect('lista_sucursales')