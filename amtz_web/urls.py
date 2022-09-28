
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from django.conf.urls import handler404
from django.contrib.sitemaps.views import sitemap
from amtz_web.sitemap import StaticViewSitemap
from django.views.generic.base import TemplateView
sitemaps = {
    'static': StaticViewSitemap,
}

import store.views.home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('', include('ourCenter.urls')),
    path('', include('ecommerce.urls')),
    path('', include('room_booking.urls')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps, 'template_name': 'sitemap.xml'},
         name='django.contrib.sitemaps.views.sitemap'),
    path("robots.txt", TemplateView.as_view(
        template_name="robots.txt", content_type="text/plain")),
]
handler404 = store.views.home.handler404
admin.site.site_header = 'ANDHRA PRADESH MED TECH ZONE'
admin.site.index_title = 'AMTZ WEBSITE ADMIN PANEL'
admin.site.site_title = 'ADMIN PANEL'

# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
