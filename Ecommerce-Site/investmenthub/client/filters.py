import django_filters
from django_filters import DateFilter, CharFilter
from product.models import *

class ProductFilter(django_filters.FilterSet):
    created = DateFilter(field_name="date_added", lookup_expr='gte')
    description = CharFilter(field_name="description", lookup_expr='icontains')
    #title = CharFilter(field_name="title", lookup_expr='icontains')
    class Meta:
        model = Product
        #fields = ['title', 'research_type', 'slug', 'description', 'price']
        fields = '__all__'
        exclude = 'file'