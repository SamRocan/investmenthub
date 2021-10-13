import django_filters
from django_filters import DateFilter, CharFilter
from product.models import *

class UserProductFilter(django_filters.FilterSet):
    name = CharFilter(label="Name", field_name="title", lookup_expr='icontains')
    price__gt = django_filters.NumberFilter(label="Min Price",field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(label="Max Price", field_name='price', lookup_expr='lt')
    class Meta:
        model = Product
        fields = ''
        exclude = ['file','client', 'slug']

class ProductFilter(django_filters.FilterSet):
    name = CharFilter(label="Name", field_name="title", lookup_expr='icontains')
    price__gt = django_filters.NumberFilter(label="Min Price",field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(label="Max Price", field_name='price', lookup_expr='lt')
    class Meta:
        model = Product
        fields = ['client']
        exclude = ['file', 'slug']