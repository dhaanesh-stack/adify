import django_filters
from django.db.models import Q
from .models import Ad, Category

class AdFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(
        method='filter_by_query',
        label='',
        widget=django_filters.widgets.forms.TextInput(
            attrs={
                "placeholder": "Search ads by title or description...",
                "class": "w-full md:w-64 p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500",
            }
        ),
    )
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        empty_label="All Categories",
        label='',
        widget=django_filters.widgets.forms.Select(
            attrs={
                "class": "w-full md:w-48 p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500",
            }
        ),
    )
    location = django_filters.CharFilter(
        lookup_expr="icontains",
        label='',
        widget=django_filters.widgets.forms.TextInput(
            attrs={
                "placeholder": "Enter location...",
                "class": "w-full md:w-48 p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500",
            }
        ),
    )
    min_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="gte",
        label='',
        widget=django_filters.widgets.forms.NumberInput(
            attrs={
                "placeholder": "Min price",
                "class": "w-28 p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500",
            }
        ),
    )
    max_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="lte",
        label='',
        widget=django_filters.widgets.forms.NumberInput(
            attrs={
                "placeholder": "Max price",
                "class": "w-28 p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500",
            }
        ),
    )

    class Meta:
        model = Ad
        fields = ['q', 'category', 'location', 'min_price', 'max_price']

    def filter_by_query(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(description__icontains=value))
