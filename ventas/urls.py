from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_venta, name='registrar_venta'),
    path('lista/', views.lista_ventas, name='lista_ventas'),
]
