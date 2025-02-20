
from django.urls import path
from . import views
from pedidos.views import obtener_datos_iniciales
from .views import *

urlpatterns = [
    path('productos/', ProductoListView.as_view(), name='Productos'),
    path('productos/add/', ProductoCreateView.as_view(), name='Prod-Add'),
    path('productos/<int:pk>/edit/', ProductoUpdateView.as_view(), name='Prod-Edit'),  
    path('productos/<int:pk>/delete/', ProductoDeleteView.as_view(), name='Prod-Delete'),  
    path('vendedores/', VendedorListView.as_view(), name='Vendedores'),
    path('vendedores/add/', VendedorCreateView.as_view(), name='Vend-Add'),
    path('vendedores/<int:pk>/edit/', VendedorUpdateView.as_view(), name='Vend-Edit'),
    path('vendedores/<int:pk>/delete/', VendedorDeleteView.as_view(), name='Vend-Delete'),
    path('clientes/', ClienteListView.as_view(), name='Clientes'),
    path('clientes/add/', ClienteCreateView.as_view(), name='Cli-Add'),
    path('clientes/<int:pk>/edit/', ClienteUpdateView.as_view(), name='Cli-Edit'), 
    path('clientes/<int:pk>/delete/', ClienteDeleteView.as_view(), name='Cli-Delete'),
    path('', lista_pedidos, name='lista_pedidos'),
    path('pedido/<int:pedido_id>/', ver_pedido, name='ver_pedido'),
    path('pedido/editar/<int:pedido_id>', agregar_productos_form, name='agregar_productos_form'),
    path('pedido/modificar/<int:pedido_id>/', actualizar_pedido, name='agregar_productos'),
    path('anular_pedido/<int:pedido_id>/', anular_pedido, name='anular_pedido'),
    path('pedido_especial/api/obtener-datos-iniciales/', obtener_datos_iniciales, name='obtener-datos-iniciales'),
    path('pedido_especial/', form_pedido_gestion, name='Ped-Form-Ges'),
    path('pedidos/imprimir/', views.pedidos_por_fecha, name='PedidosPorFecha'),
    path('pedidos/liquidacion/', views.pedidos_liquidacion, name='PedidosLiquidacion'),
]