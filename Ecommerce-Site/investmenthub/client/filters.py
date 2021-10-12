import django_filters
from django_filters import DateFilter, CharFilter
from product.models import *

class UserProductFilter(django_filters.FilterSet):
    description = CharFilter(field_name="description", lookup_expr='icontains')
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    class Meta:
        model = Product
        fields = ''
        exclude = ['file','client', 'slug']

class ProductFilter(django_filters.FilterSet):
    description = CharFilter(field_name="description", lookup_expr='icontains')
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    class Meta:
        model = Product
        fields = ''
        exclude = ['file', 'slug']