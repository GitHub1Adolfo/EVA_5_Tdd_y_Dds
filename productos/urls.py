from django.urls import path
from . import views

urlpatterns = [
    path('inventario/', views.inventario_view, name='inventario'),
    path('agregar/', views.agregar_producto, name='agregar_producto'),
    path('editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('alertas/', views.alertas_view, name='alertas'),
    path('transferencias/', views.listar_transferencias, name='listar_transferencias'),
    path('transferencias/nueva/', views.transferir_producto, name='transferir_producto'),
    path('transferencias/<int:transferencia_id>/<str:accion>/', views.actualizar_transferencia, name='actualizar_transferencia'),
]