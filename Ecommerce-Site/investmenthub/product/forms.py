from django.forms import ModelForm,TextInput, Textarea, Select

from .models import Product, ProductFile

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'research_type', 'slug', 'description', 'price', 'file']
        widgets = {
            'title': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Name'
            }),
            'research_type': Select(
                attrs={
                    'class': "form-select",
                    'style': 'max-width: 300px;',
                }
            ),
            'slug': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Product Slug (no spaces)'
            }),
            'description': Textarea(attrs={
                'class':"form-control",
                'style':'max-width: 300px; min-height:100px;',
                'placeholder':'Describe the product here...'
            }),
        }
class ProductImageForm(ModelForm):
    class Meta:
        model = ProductFile
        fields = ['file']