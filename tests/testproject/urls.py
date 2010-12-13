from django import VERSION
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin


admin.autodiscover()

try:
    import registration.backends
except ImportError:
    urlpatterns = patterns('',
        (r'^accounts/', include('registration.urls')),
    )
else:
    urlpatterns = patterns('',
        (r'^accounts/', include('registration.backends.default.urls')),
    )

urlpatterns += patterns('',
    (r'^', include('testproject.testapp.urls')),
)

if VERSION >= (1, 1):
    urlpatterns += patterns('',
        (r'^admin/', include(admin.site.urls)),
    )
else:
    urlpatterns += patterns('',
        (r'^admin/(.*)', admin.site.root),
    )

if settings.DEBUG:
    if VERSION >= (1, 3):
        static_root = settings.STATIC_ROOT
        static_url = settings.STATIC_URL
        static_view = 'django.contrib.staticfiles.views.serve'
    else:
        static_root = settings.MEDIA_ROOT
        static_url = settings.MEDIA_URL
        static_view = 'django.views.static.serve'

    if static_url.startswith('/'):
        urlpatterns += patterns('',
            (r'^%s/(?P<path>.*)' % static_url.strip('/'), static_view,
             {'document_root': static_root}),
        )
