from django_filters import rest_framework as filters

from books.models import Book


class BookFilter(filters.FilterSet):
    author = filters.CharFilter(
        field_name='author', lookup_expr='icontains',  label='Автор книги'
    )
    year = filters.NumberFilter(
        field_name='year', lookup_expr='exact',  label='Год издания'
    )
    department = filters.CharFilter(
        field_name='department__name',
        lookup_expr='icontains',
        label='Название отдела'
    )
    available = filters.BooleanFilter(
        method='filter_available', label='Наличие книги'
    )

    class Meta:
        model = Book
        fields = ['author', 'year', 'department', 'available']

    def filter_available(self, queryset, name, value):
        if value:
            return queryset.filter(count__gt=0)
        return queryset.filter(count=0)
