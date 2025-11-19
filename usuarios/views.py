from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Usuario
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from sucursales.models import Sucursal
from django.core.exceptions import PermissionDenied

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.rol == 'administrador':
                return redirect('dashboard_admin')
            else:
                return redirect('dashboard_vendedor')
        else:
            return render(request, 'usuarios/login.html', {'error': 'Credenciales incorrectas'})
    return render(request, 'usuarios/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_admin(request):
    if request.user.rol != 'administrador':
        raise PermissionDenied 
    return render(request, 'usuarios/dashboard_admin.html')

@login_required
def dashboard_vendedor(request):
    if request.user.rol != 'vendedor':
        raise PermissionDenied 
    return render(request, 'usuarios/dashboard_vendedor.html')


@login_required
def lista_usuarios(request):
    if request.user.rol != 'administrador':
        raise PermissionDenied
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})


@login_required(login_url='login')
def inicio_view(request):
    if request.user.rol == 'administrador':
        destino = reverse('dashboard_admin')
    elif request.user.rol == 'vendedor':
        destino = reverse('dashboard_vendedor')
    else:
        destino = reverse('login')

    return render(request, 'usuarios/inicio.html', {'destino': destino})

@login_required
def agregar_usuario(request):
    if request.user.rol != 'administrador':
        return redirect('dashboard_vendedor')

    sucursales = Sucursal.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        password = make_password(request.POST['password'])
        rol = request.POST['rol']
        sucursal_id = request.POST.get('sucursal')

        sucursal = Sucursal.objects.get(id=sucursal_id) if sucursal_id else None

        Usuario.objects.create(username=username, password=password, rol=rol, sucursal=sucursal)
        return redirect('lista_usuarios')

    return render(request, 'usuarios/agregar_usuario.html', {'sucursales': sucursales})



@login_required
def editar_usuario(request, id):
    if request.user.rol != 'administrador':
        return redirect('dashboard_vendedor')

    user = Usuario.objects.get(id=id)
    sucursales = Sucursal.objects.all()

    if request.method == 'POST':
        user.username = request.POST['username']
        user.rol = request.POST['rol']
        sucursal_id = request.POST.get('sucursal')
        user.sucursal = Sucursal.objects.get(id=sucursal_id) if sucursal_id else None
        user.save()
        return redirect('lista_usuarios')

    return render(request, 'usuarios/editar_usuario.html', {'user': user, 'sucursales': sucursales})

@login_required
def eliminar_usuario(request, id):
    if request.user.rol != 'administrador':
        return redirect('dashboard_vendedor')

    user = Usuario.objects.get(id=id)
    user.delete()
    return redirect('lista_usuarios')