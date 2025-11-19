from django.shortcuts import render, redirect,get_object_or_404
from .models import Producto, Inventario
from django.contrib.auth.decorators import login_required
from .models import Producto
from django.db.models import F
from sucursales.models import Sucursal
from django.contrib import messages
from .models import Producto, Inventario, Transferencia
from django.db import transaction
from django.views.decorators.http import require_POST

@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/inventario.html', {'productos': productos})

@login_required
def agregar_producto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip().lower()
        categoria = request.POST.get('categoria', '').strip()
        codigo_barras = request.POST.get('codigo_barras', '').strip()
        precio = request.POST.get('precio') or 0
        stock_inicial = int(request.POST.get('stock') or 0)
        stock_minimo = int(request.POST.get('stock_minimo') or 0)

        if request.user.rol == 'vendedor':
            sucursal = request.user.sucursal
        else:
            sucursal_id = request.POST.get('sucursal')
            sucursal = get_object_or_404(Sucursal, id=sucursal_id) if sucursal_id else None

        if not nombre or not sucursal:
            messages.error(request, "Debe completar todos los campos obligatorios.")
            return redirect('agregar_producto')

        producto, creado = Producto.objects.get_or_create(
            nombre=nombre,
            defaults={
                'categoria': categoria,
                'precio': precio,
                'stock_minimo': stock_minimo,
            }
        )

        if not creado:
            producto.categoria = categoria
            producto.precio = precio
            producto.stock_minimo = stock_minimo
            producto.save()

        inventario, inv_creado = Inventario.objects.get_or_create(
            producto=producto,
            sucursal=sucursal,
            defaults={'stock': stock_inicial}
        )
        
        if not inv_creado:
            inventario.stock += stock_inicial
            inventario.save()

        messages.success(request, f"✅ Producto '{producto.nombre}' agregado o actualizado en {sucursal.nombre}.")
        return redirect('inventario')

    sucursales = Sucursal.objects.all() if request.user.rol == 'administrador' else None
    return render(request, 'productos/agregar.html', {'sucursales': sucursales})



@login_required
def ventas_view(request):
    return render(request, 'productos/ventas.html')

@login_required
def inventario_view(request):
    if request.user.rol == 'administrador':
        productos = Inventario.objects.select_related('producto', 'sucursal').all()
        transferencias = Transferencia.objects.all()
    else:
        sucursal_usuario = request.user.sucursal
        if not sucursal_usuario:
            productos = []
            transferencias = []
        else:
            productos = Inventario.objects.select_related('producto', 'sucursal').filter(sucursal=sucursal_usuario)
            transferencias = Transferencia.objects.filter(sucursal_destino=sucursal_usuario, estado='pendiente')

    return render(request, 'productos/inventario.html', {
        'productos': productos,
        'transferencias': transferencias
    })


@login_required
def alertas_view(request):
    sucursal_usuario = request.user.sucursal
    alertas = Inventario.objects.filter(
        sucursal=sucursal_usuario,
        stock__lte=F('producto__stock_minimo')
    )
    return render(request, 'productos/alertas.html', {'productos': alertas})

@login_required
@transaction.atomic
def editar_producto(request, producto_id):
    prod = get_object_or_404(Producto, id=producto_id)

    inventarios = Inventario.objects.select_related('sucursal').filter(producto=prod)

    if request.method == 'POST':
        nuevo_nombre = request.POST.get('nombre', '').strip().lower()
        nueva_categoria = request.POST.get('categoria', '').strip()
        nuevo_precio = request.POST.get('precio') or 0
        nuevo_minimo = int(request.POST.get('stock_minimo') or 0)

        existente = Producto.objects.filter(nombre=nuevo_nombre).exclude(id=prod.id).first()
        if existente:
            messages.error(request, f"❌ Ya existe un producto con el nombre '{nuevo_nombre}'.")
            return redirect('editar_producto', producto_id=producto_id)

        prod.nombre = nuevo_nombre
        prod.categoria = nueva_categoria
        prod.precio = nuevo_precio
        prod.stock_minimo = nuevo_minimo
        prod.save()

        messages.success(request, "✅ Producto actualizado correctamente.")
        return redirect('inventario')

    return render(request, 'productos/editar.html', {
        'producto': prod,
        'inventarios': inventarios
    })



@login_required
def transferir_producto(request):
    if request.user.rol != 'administrador':
        return render(request, '403.html', status=403)

    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        origen_id = request.POST.get('sucursal_origen')
        destino_id = request.POST.get('sucursal_destino')
        cantidad = int(request.POST.get('cantidad'))

        producto = get_object_or_404(Producto, id=producto_id)
        suc_origen = get_object_or_404(Sucursal, id=origen_id)
        suc_destino = get_object_or_404(Sucursal, id=destino_id)

        if origen_id == destino_id:
            messages.error(request, "⚠️ No puedes transferir a la misma sucursal.")
            return redirect('transferir_producto')

        inventario_origen = Inventario.objects.filter(producto=producto, sucursal=suc_origen).first()

        if not inventario_origen or inventario_origen.stock < cantidad:
            messages.error(request, "⚠️ Stock insuficiente en la sucursal origen.")
            return redirect('transferir_producto')

        with transaction.atomic():
            inventario_origen.stock -= cantidad
            inventario_origen.save()

            Transferencia.objects.create(
                producto=producto,
                sucursal_origen=suc_origen,
                sucursal_destino=suc_destino,
                cantidad=cantidad,
                estado='pendiente'
            )

        messages.success(request, f"📦 Transferencia de {cantidad} {producto.nombre} creada (Pendiente).")
        return redirect('listar_transferencias')
    
    producto_preseleccionado = request.GET.get('producto')
    origen_preseleccionado = request.GET.get('origen')

    productos = Producto.objects.all()
    sucursales = Sucursal.objects.all()

    return render(request, 'productos/transferir.html', {
        'productos': productos,
        'sucursales': sucursales,
        'producto_preseleccionado': producto_preseleccionado,
        'origen_preseleccionado': origen_preseleccionado,
    })

@login_required
def listar_transferencias(request):
    if request.user.rol == 'vendedor':
        transferencias = Transferencia.objects.filter(
            sucursal_destino=request.user.sucursal
        ).order_by('-fecha')
    else:
        transferencias = Transferencia.objects.all().order_by('-fecha')

    return render(request, 'productos/transferencias.html', {'transferencias': transferencias})


@login_required
def actualizar_transferencia(request, transferencia_id, accion):
    transferencia = get_object_or_404(Transferencia, id=transferencia_id)

    if request.user.sucursal != transferencia.sucursal_destino:
        messages.error(request, "No tienes permiso para actualizar esta transferencia.")
        return redirect('inventario')

    if accion == 'aceptar':
        inventario_destino, _ = Inventario.objects.get_or_create(
            producto=transferencia.producto,
            sucursal=transferencia.sucursal_destino,
            defaults={'stock': 0}
        )
        inventario_destino.stock += transferencia.cantidad
        inventario_destino.save()

        transferencia.estado = 'aceptada'
        transferencia.save()
        messages.success(request, f"Transferencia de {transferencia.cantidad} unidades de {transferencia.producto.nombre} aceptada.")
    elif accion == 'rechazar':
        transferencia.estado = 'rechazada'
        transferencia.save()
        messages.warning(request, "Transferencia rechazada.")

    return redirect('inventario')


