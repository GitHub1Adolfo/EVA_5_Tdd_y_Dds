from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_sucursales, name='lista_sucursales'),
    path('agregar/', views.agregar_sucursal, name='agregar_sucursal'),
    path('editar/<int:id>/', views.editar_sucursal, name='editar_sucursal'),
    path('eliminar/<int:id>/', views.eliminar_sucursal, name='eliminar_sucursal'),
]