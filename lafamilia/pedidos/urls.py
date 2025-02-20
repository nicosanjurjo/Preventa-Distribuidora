from django.urls import path
from . import views


urlpatterns = [
    path('', views.pedidos, name='Ped-Form'),
    path('api/obtener-datos-iniciales/', views.obtener_datos_iniciales, name='obtener-datos-iniciales'),
    path('crear/', views.crear_pedido, name='crear_pedido'),
    path('clientes/add/', views.ClienteCreateView.as_view(), name='Cli-Add')

]