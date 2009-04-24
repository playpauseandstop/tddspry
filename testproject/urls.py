from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    (r'^accounts/', include('registration.urls')),
    (r'^', include('testproject.testapp.urls')),
    url(r'^admin/(.*)', admin.site.root),
)

if settings.DEBUG and settings.MEDIA_URL.startswith('/'):
    urlpatterns += patterns('django.views.static',
        (r'^%s/(?P<path>.*)' % settings.MEDIA_URL.strip('/'), 'serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
