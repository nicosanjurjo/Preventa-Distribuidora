from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from .models import Producto, Vendedor, Cliente, Pedido, PedidoProducto
from .forms import ProductoForm, VendedorForm, ClienteForm
from django.http import JsonResponse, response
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib import messages

class ProductoListView(ListView):
    model = Producto
    template_name = 'gestion/prod.html'
    context_object_name = 'productos'

class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'gestion/prod-form.html'
    success_url = reverse_lazy('Productos')

class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'gestion/prod-form.html'
    success_url = reverse_lazy('Productos')

class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'gestion/prod-delete.html'
    success_url = reverse_lazy('Productos')

class VendedorListView(ListView):
    model = Vendedor
    template_name = 'gestion/vend.html'
    context_object_name = 'vendedores'

class VendedorCreateView(CreateView):
    model = Vendedor
    form_class = VendedorForm
    template_name = 'gestion/vend-form.html'
    success_url = reverse_lazy('Vendedores')

class VendedorUpdateView(UpdateView):
    model = Vendedor
    form_class = VendedorForm
    template_name = 'gestion/vend-form.html'
    success_url = reverse_lazy('Vendedores')

class VendedorDeleteView(DeleteView):
    model = Vendedor
    template_name = 'gestion/vend-delete.html'
    success_url = reverse_lazy('Vendedores')

class ClienteListView(ListView):
    model = Cliente
    template_name = 'gestion/cli.html'
    context_object_name = 'clientes'

class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'gestion/cli-form.html'
    success_url = reverse_lazy('Clientes')

class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'gestion/cli-form.html'
    success_url = reverse_lazy('Clientes')

class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'gestion/cli-delete.html'
    success_url = reverse_lazy('Clientes')

def lista_pedidos(request):
    pedidos = Pedido.objects.all().order_by('-fecha')
    vendedores = Vendedor.objects.all()
    clientes = Cliente.objects.all()
    return render(request, 'gestion/ped.html', {'pedidos': pedidos, 'vendedores': vendedores, 'clientes': clientes})

def ver_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    productos_pedido = PedidoProducto.objects.filter(pedido=pedido)
    
    context = {
        'pedido': pedido,
        'productos_pedido': productos_pedido,
    }
    
    return render(request, 'gestion/ped-detalle.html', context)

def form_pedido_gestion(request):
    return render(request, 'gestion/ped-form.html')

def pedidos_por_fecha(request):
    # Obtener los datos del formulario
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')
    vendedor_id = request.GET.get('vendedor')
    cliente_id = request.GET.get('cliente')
    diareparto = request.GET.get('diareparto')
    
    # Filtros básicos de fecha
    if fecha_inicio_str:
        fecha_inicio = timezone.make_aware(datetime.strptime(fecha_inicio_str, '%Y-%m-%d'))
    else:
        fecha_inicio = None
        
    if fecha_fin_str:
        fecha_fin = timezone.make_aware(datetime.strptime(fecha_fin_str, '%Y-%m-%d')) + timedelta(days=1) - timedelta(seconds=1)
    else:
        fecha_fin = None

    # Base de la consulta de pedidos
    pedidos = Pedido.objects.all()
    pedidos = pedidos.filter(anulado=False)
    
    # Filtrar por rango de fechas si las fechas están disponibles
    if fecha_inicio and fecha_fin:
        pedidos = pedidos.filter(fecha__range=[fecha_inicio, fecha_fin])
    elif fecha_inicio:
        pedidos = pedidos.filter(fecha__gte=fecha_inicio)
    elif fecha_fin:
        pedidos = pedidos.filter(fecha__lte=fecha_fin)

    # Filtro por vendedor
    if vendedor_id:
        pedidos = pedidos.filter(vendedor_id=vendedor_id)
    
    # Filtro por cliente
    if cliente_id:
        pedidos = pedidos.filter(cliente_id=cliente_id)
    
    # Filtro por día de reparto
    if diareparto:
        pedidos = pedidos.filter(diareparto=diareparto)
    
    # Renderizar la plantilla con los pedidos filtrados
    return render(request, 'gestion/ped-imprimir.html', {'pedidos': pedidos})

def pedidos_liquidacion(request):
    # Obtener los datos del formulario
    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')
    vendedor_id = request.GET.get('vendedor')
    cliente_id = request.GET.get('cliente')
    diareparto = request.GET.get('diareparto')
    
    # Filtros básicos de fecha
    if fecha_inicio_str:
        fecha_inicio = timezone.make_aware(datetime.strptime(fecha_inicio_str, '%Y-%m-%d'))
    else:
        fecha_inicio = None
        
    if fecha_fin_str:
        fecha_fin = timezone.make_aware(datetime.strptime(fecha_fin_str, '%Y-%m-%d')) + timedelta(days=1) - timedelta(seconds=1)
    else:
        fecha_fin = None

    # Base de la consulta de pedidos
    pedidos = Pedido.objects.all()
    pedidos = pedidos.filter(anulado=False)
    
    # Filtrar por rango de fechas si las fechas están disponibles
    if fecha_inicio and fecha_fin:
        pedidos = pedidos.filter(fecha__range=[fecha_inicio, fecha_fin])
    elif fecha_inicio:
        pedidos = pedidos.filter(fecha__gte=fecha_inicio)
    elif fecha_fin:
        pedidos = pedidos.filter(fecha__lte=fecha_fin)

    # Filtro por vendedor
    if vendedor_id:
        pedidos = pedidos.filter(vendedor_id=vendedor_id)
        vendedores = Vendedor.objects.filter(id=vendedor_id).values_list('nombre', flat=True)
    else:
        vendedores = Vendedor.objects.all().values_list('nombre', flat=True)
    
    # Filtro por cliente
    if cliente_id:
        pedidos = pedidos.filter(cliente_id=cliente_id)
    
    # Filtro por día de reparto
    if diareparto:
        pedidos = pedidos.filter(diareparto=diareparto)
    
    # Calcular el total de todos los pedidos filtrados
    total_pedidos = sum(pedido.total for pedido in pedidos)

    # Renderizar la plantilla con los pedidos filtrados, fechas, vendedores y total
    contexto = {
        'pedidos': pedidos,
        'fecha_inicio': fecha_inicio_str,
        'fecha_fin': fecha_fin_str,
        'vendedores': vendedores,
        'total_pedidos': total_pedidos,
    }

    return render(request, 'gestion/ped-liquidacion.html', contexto)


@csrf_exempt
def agregar_productos_form(request, pedido_id):
    # Obtener el pedido por su ID, o devolver un 404 si no existe
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    # Recoger los datos asociados al pedido
    cliente = pedido.cliente
    vendedor = pedido.vendedor
    fecha = pedido.fecha
    productos = Producto.objects.all()
    marcas = list(Producto.objects.values_list('marca', flat=True).distinct())

    # Pasar estos datos al template para renderizar
    context = {
        'pedido': pedido,
        'cliente': cliente,
        'vendedor': vendedor,
        'fecha': fecha,
        'productos': productos,
        'marcas': marcas
    }
    
    return render(request, 'gestion/ped-editar-form.html', context)

@csrf_exempt
def actualizar_pedido(request, pedido_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            pedido = Pedido.objects.get(id=pedido_id)
            productos_data = data['productos']
            nuevo_total = data['total']  # Total calculado desde el frontend

            # Sumamos el nuevo total al total existente
            pedido.total += nuevo_total

            errores_stock = []
            
            # Recorrer cada producto enviado para la actualización
            for item in productos_data:
                producto = Producto.objects.get(id=item['producto_id'])
                cantidad = item['cantidad']
                precio_unitario = item['precio_unitario']

                # Verificar si el producto ya está en el pedido
                pedido_producto, creado = PedidoProducto.objects.get_or_create(
                    pedido=pedido,
                    producto=producto,
                    defaults={'cantidad': cantidad, 'precio_unitario': precio_unitario}
                )

                if creado:
                    # Si es un nuevo producto en el pedido, simplemente descontamos el stock
                    if producto.stock >= cantidad:
                        producto.stock -= cantidad
                        producto.save()
                    else:
                        errores_stock.append(f"{producto.nombre} - {producto.marca}. Disponible: {producto.stock}, solicitado: {cantidad}.")
                else:
                    # Si ya existe, actualizamos la cantidad y descontamos la nueva cantidad
                    cantidad_total = pedido_producto.cantidad + cantidad

                    if producto.stock >= cantidad:
                        producto.stock -= cantidad
                        producto.save()
                        pedido_producto.cantidad = cantidad_total
                        pedido_producto.precio_unitario = precio_unitario
                        pedido_producto.save()
                    else:
                        errores_stock.append(f"{producto.nombre} - {producto.marca}. Disponible: {producto.stock}, solicitado: {cantidad}.")
            
            # Si hay errores de stock, devolvemos los errores sin eliminar productos ya existentes
            if errores_stock:
                return JsonResponse({'errors': errores_stock}, status=400)

            # Actualizar el total del pedido
            pedido.modificado=True
            pedido.save()

            return JsonResponse({'message': 'Pedido actualizado exitosamente'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def anular_pedido(request, pedido_id):
    # Obtener el pedido usando el pedido_id
    pedido = get_object_or_404(Pedido, id=pedido_id)

    # Verificar si el pedido ya está anulado
    if pedido.anulado:
        return JsonResponse({'error': 'El pedido ya está anulado'}, status=400)

    # Marcar el pedido como anulado
    pedido.anulado = True
    pedido.save()

    # Obtener todos los productos relacionados con el pedido
    pedido_productos = PedidoProducto.objects.filter(pedido=pedido)

    # Sumar la cantidad de cada producto al stock
    for pedido_producto in pedido_productos:
        producto = pedido_producto.producto
        producto.stock += pedido_producto.cantidad
        producto.save()

    # Retornar una respuesta exitosa
    return JsonResponse({'success': f'El pedido #{pedido_id} ha sido anulado y el stock ha sido actualizado.'})