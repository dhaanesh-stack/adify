import django_filters
from django.db.models import Q
from .models import Ad, Category

class AdFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='filter_by_query', label='Search')
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(), empty_label="All Categories"
    )
    location = django_filters.CharFilter(lookup_expr='icontains', label='Location')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Min Price')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Max Price')

    class Meta:
        model = Ad
        fields = ['q', 'category', 'location', 'min_price', 'max_price']

    def filter_by_query(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(description__icontains=value))
