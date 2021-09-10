from django_filters import rest_framework as filters

from reviews.models import Title


class CustomFilter(filters.FilterSet):
    genre = filters.CharFilter(field_name='genre__slug', lookup_expr='iexact')
    category = filters.CharFilter(field_name='category__slug',
                                  lookup_expr='iexact')
    name = filters.CharFilter(field_name='name', lookup_expr='contains')
    year = filters.NumberFilter(field_name='year', lookup_expr='iexact')

    class Meta:
        model = Title
        fields = ('genre', 'category', 'year', 'name')
