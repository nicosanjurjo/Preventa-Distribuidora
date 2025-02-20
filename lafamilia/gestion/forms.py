from django import forms
from .models import Producto, Vendedor, Cliente


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['marca', 'nombre', 'descripcion', 'precio', 'codigo', 'stock']

class VendedorForm(forms.ModelForm):
    class Meta:
        model = Vendedor
        fields = ['nombre', 'dni']

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'direccion', 'telefono']


