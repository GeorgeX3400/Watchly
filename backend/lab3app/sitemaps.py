from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Watch

class WatchSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return Watch.objects.all()
    
    def lastmod(self, obj):
        return obj.updatedAt


class StaticViewsSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.4

    def items(self):
        return ['contact', 'register', 'login', 'home']
    
    def location(self, item):
        return reverse(item)
    