from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_view, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard/vendedor/', views.dashboard_vendedor, name='dashboard_vendedor'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/agregar/', views.agregar_usuario, name='agregar_usuario'),
    path('usuarios/editar/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),

]