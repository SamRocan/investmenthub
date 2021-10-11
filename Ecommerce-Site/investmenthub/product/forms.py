from django.forms import ModelForm

from .models import Product, ProductFile

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'research_type', 'slug', 'description', 'price', 'file']

class ProductImageForm(ModelForm):
    class Meta:
        model = ProductFile
        fields = ['file']