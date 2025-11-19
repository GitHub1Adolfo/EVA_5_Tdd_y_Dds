from django.urls import path
from . import views

urlpatterns = [
    path('stock/', views.reportes_stock, name='reportes_stock'),
    path('ventas/', views.reportes_ventas, name='reportes_ventas'),
    path('dashboard/', views.reportes_dashboard, name='reportes_dashboard'),
]
