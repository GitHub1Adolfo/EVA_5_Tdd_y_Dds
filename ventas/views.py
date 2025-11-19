from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from productos.models import Producto
from .models import Venta

from productos.models import Inventario

@login_required
def registrar_venta(request):
    sucursal = request.user.sucursal
    productos = Inventario.objects.filter(sucursal=sucursal)

    if request.method == 'POST':
        inventario_id = request.POST.get('producto')
        cantidad = int(request.POST.get('cantidad'))

        inventario = Inventario.objects.get(id=inventario_id)
        producto = inventario.producto
        total = producto.precio * cantidad

        if inventario.stock >= cantidad:
            inventario.stock -= cantidad
            inventario.save()

            Venta.objects.create(
                producto=producto,
                cantidad=cantidad,
                total=total,
                vendedor=request.user
            )
            return redirect('lista_ventas')
        else:
            error = "No hay suficiente stock disponible en esta sucursal."
            return render(request, 'ventas/registrar.html', {
                'productos': productos,
                'error': error
            })

    return render(request, 'ventas/registrar.html', {'productos': productos})



@login_required
def lista_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha')
    return render(request, 'ventas/lista.html', {'ventas': ventas})
