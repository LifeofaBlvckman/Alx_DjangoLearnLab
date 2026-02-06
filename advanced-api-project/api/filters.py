import django_filters
from .models import Book


class BookFilter(django_filters.FilterSet):
    """
    FilterSet for Book model with advanced filtering options.
    """
    title = django_filters.CharFilter(
        lookup_expr='icontains', 
        help_text="Filter by title (case-insensitive, partial match)"
    )
    publication_year = django_filters.NumberFilter(
        help_text="Filter by exact publication year"
    )
    publication_year__gt = django_filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='gt',
        help_text="Filter by publication year greater than"
    )
    publication_year__lt = django_filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='lt',
        help_text="Filter by publication year less than"
    )
    author__name = django_filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains',
        help_text="Filter by author name (case-insensitive, partial match)"
    )
    
    class Meta:
        model = Book
        fields = []
