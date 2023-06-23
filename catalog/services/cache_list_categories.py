from django.conf import settings
from django.core.cache import cache
from ..models import Category


def get_all_categories():
    if settings.CACHE_ENABLED:
        key = 'category_list'
        categories = cache.get(key)
        if categories is None:
            categories = list(Category.objects.all())
            cache.set(key, categories)
    else:
        categories = list(Category.objects.all())
    return categories
