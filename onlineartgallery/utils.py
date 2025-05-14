from artworks.models import Artwork

def get_common_artwork_data():
    """Utility function to get common artwork data used across apps"""
    all_categories = Artwork.objects.filter(status='approved').values_list('category', flat=True).distinct()
    return {
        'all_categories': all_categories,
    }

def apply_artwork_filters(queryset, filters):
    """Apply filters to artwork queryset"""
    category = filters.get('category', '')
    price_range = filters.get('price_range', '')
    sort_by = filters.get('sort_by', '')

    if category:
        queryset = queryset.filter(category=category)

    if price_range:
        if price_range == '0-10000':
            queryset = queryset.filter(price__lte=10000)
        elif price_range == '10000-50000':
            queryset = queryset.filter(price__gt=10000, price__lte=50000)
        elif price_range == '50000+':
            queryset = queryset.filter(price__gt=50000)

    if sort_by:
        if sort_by == 'price_low':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_high':
            queryset = queryset.order_by('-price')
    else:
        queryset = queryset.order_by('-created_at')

    return queryset