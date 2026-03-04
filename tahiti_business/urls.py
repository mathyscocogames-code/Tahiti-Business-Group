from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from django.http import HttpResponse
from django.views.generic import TemplateView

handler404 = 'ads.views.custom_404'


def robots_txt(request):
    base = request.build_absolute_uri('/')
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /admin/\n"
        "Disallow: /admin-stats/\n"
        "Disallow: /rubriques/moderation/\n"
        f"Sitemap: {base}sitemap.xml\n"
    )
    return HttpResponse(content, content_type='text/plain')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ads.urls')),
    path('users/', include('users.urls')),
    path('pubs/', include('pubs.urls')),
    path('rubriques/', include('rubriques.urls')),
    path('robots.txt', robots_txt),
    path('sitemap.xml', TemplateView.as_view(
        template_name='sitemap.xml',
        content_type='application/xml',
    )),
]

# Serve media files in all environments (DEBUG=True and DEBUG=False)
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
