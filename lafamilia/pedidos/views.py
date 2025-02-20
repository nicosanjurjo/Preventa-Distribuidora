from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from gestion.models import Producto, Vendedor, Cliente, Pedido, PedidoProducto
from django.views.generic import CreateView
from gestion.forms import ClienteForm
from django.urls import reverse_lazy
import json
from django.views.decorators.csrf import csrf_exempt


def pedidos(request):
    return render(request, 'pedidos/ped-form.html')


def obtener_datos_iniciales(request):
    try:
        vendedores = list(Vendedor.objects.values('id', 'nombre'))
        clientes = list(Cliente.objects.values('id', 'nombre', 'direccion'))
        productos = list(Producto.objects.values('id', 'nombre', 'marca', 'precio'))
        marcas = list(Producto.objects.values_list('marca', flat=True).distinct())

        data = {
            'vendedores': vendedores,
            'clientes': clientes,
            'productos': productos,
            'marcas': marcas
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@csrf_exempt
def crear_pedido(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            if not data.get('cliente_id') or not data.get('productos') or not data.get('diareparto'):
                return JsonResponse({'error': 'Faltan datos obligatorios (cliente, productos, o dia de reparto)'}, status=400)

            cliente = Cliente.objects.get(id=data['cliente_id'])
            vendedor = Vendedor.objects.get(id=data['vendedor_id']) if data.get('vendedor_id') else None
            diareparto = data.get('diareparto')
            observaciones = data.get('observaciones')
            total = data['total']

            # Crear el pedido
            pedido = Pedido(vendedor=vendedor, cliente=cliente, diareparto=diareparto, observaciones=observaciones, total=total)
            pedido.save()

            errores_stock = []
            productos_a_agregar = []

            for item in data['productos']:
                producto = Producto.objects.get(id=item['producto_id'])
                cantidad = item['cantidad']
                precio_unitario = item['precio_unitario']

                if producto.stock >= cantidad:
                    productos_a_agregar.append((producto, cantidad, precio_unitario))
                else:
                    errores_stock.append(f"{producto.nombre} - {producto.marca}. Disponible: {producto.stock}, solicitado: {cantidad}.")

            if errores_stock:
                errores_stock.insert(0, "No hay suficiente stock para:")
                pedido.delete()
                return JsonResponse({'errors': errores_stock}, status=400)

            # Guardar cada producto en PedidoProducto
            for producto, cantidad, precio_unitario in productos_a_agregar:
                producto.stock -= cantidad
                producto.save()
                PedidoProducto.objects.create(pedido=pedido, producto=producto, cantidad=cantidad, precio_unitario=precio_unitario)

            return JsonResponse({'message': 'Pedido creado exitosamente'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)



class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'pedidos/cli-form.html'
    success_url = reverse_lazy('Ped-Form')


