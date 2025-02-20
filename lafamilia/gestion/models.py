from django.db import models

class Producto(models.Model):
    marca=models.CharField(max_length=20, blank=True)
    nombre=models.CharField(max_length=20)
    descripcion=models.CharField(max_length=50, blank=True)
    precio=models.IntegerField()
    codigo=models.IntegerField(unique=True)
    stock=models.IntegerField()
    
    def __str__(self):
        return self.nombre

class Vendedor(models.Model):
    nombre=models.CharField(max_length=30)
    dni=models.IntegerField(unique=True, default=99999999)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=30)
    direccion = models.CharField(max_length=30)
    telefono = models.IntegerField(null=True)

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    DIAS_REPARTO = [
        ('Lunes', 'Lunes'),
        ('Miércoles', 'Miércoles'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
    ]
    
    fecha = models.DateTimeField(auto_now_add=True)
    modificado = models.BooleanField(default=False, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, null=True)
    total = models.IntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='PedidoProducto')
    diareparto = models.CharField(max_length=10, choices=DIAS_REPARTO, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    anulado = models.BooleanField(blank=False, null=False, default=False)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nombre}"


class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.IntegerField()
    agregado = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ('pedido', 'producto')

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Pedido #{self.pedido.id}"
    

