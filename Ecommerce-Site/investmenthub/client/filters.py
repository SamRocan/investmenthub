import django_filters

from product.models import *

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['title', 'research_type', 'slug', 'description', 'price']
