from django.core.cache import cache

from blog.models import Blog
from config.settings import CACHE_ENABLED


def get_articles_from_cache():
    if not CACHE_ENABLED:
        return Blog.objects.all()
    else:
        key = 'blog_articles'
        articles = cache.get(key)
        if articles is not None:
            return articles
        else:
            articles = Blog.objects.all()
            cache.set(key, articles)
            return articles
