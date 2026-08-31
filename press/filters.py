import django_filters
from .models import Article


class ArticleFilter(django_filters.FilterSet):
    """
    Filters articles by tags, words the title contains and the date
    they were posted, with a choice of how to sort the results.
    """
    title = django_filters.CharFilter(lookup_expr='icontains',
                                      label='Title contains')
    created_on = django_filters.DateFromToRangeFilter(
        label='Posted between',
        widget=django_filters.widgets.RangeWidget(attrs={'type': 'date'}))
    ordering = django_filters.OrderingFilter(
        label='Sort by',
        choices=(
            ('-created_on', 'Newest first'),
            ('created_on', 'Oldest first'),
        ),
    )

    class Meta:
        model = Article
        fields = ['tags']
