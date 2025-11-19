from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from productos.models import Producto
from ventas.models import Venta
from django.db.models import Sum, F

@login_required
def reportes_stock(request):
    stock_bajo = Producto.objects.filter(stock__lte=F('stock_minimo'))
    return render(request, 'reportes/stock_bajo.html', {'stock_bajo': stock_bajo})


@login_required
def reportes_ventas(request):
    total_ventas = Venta.objects.aggregate(Sum('total'))['total__sum'] or 0
    ventas_por_producto = (
        Venta.objects.values('producto__nombre')
        .annotate(total_vendido=Sum('cantidad'), monto_total=Sum('total'))
        .order_by('-monto_total')
    )
    return render(request, 'reportes/ventas.html', {
        'total_ventas': total_ventas,
        'ventas_por_producto': ventas_por_producto,
    })


@login_required
def reportes_dashboard(request):

    total_productos = Producto.objects.count()
    total_ventas = Venta.objects.aggregate(Sum('total'))['total__sum'] or 0
    total_vendidos = Venta.objects.aggregate(Sum('cantidad'))['cantidad__sum'] or 0

    contexto = {
        'total_productos': total_productos,
        'total_ventas': total_ventas,
        'total_vendidos': total_vendidos,
    }
    return render(request, 'reportes/dashboard.html', contexto)
