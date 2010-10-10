from django.conf.urls.defaults import *


urlpatterns = patterns('testproject.testapp.views',
    url(r'^$', 'index', name='index'),
    url(r'^edit-hidden-fields/$', 'edit_hidden_fields',
        name='edit_hidden_fields'),
    url(r'^error/$', 'error', name='server_error'),
    url(r'^fast-redirect/$', 'fast_redirect', name='fast_redirect'),
    url(r'^login/$', 'login', name='auth_login'),
    url(r'^logout/$', 'logout', name='auth_logout'),
    url(r'^multiply-forms/$', 'multiply_forms', name='multiply_forms'),
    url(r'^profile/$', 'profile', name='profile'),
    url(r'^redirect/$', 'redirect', name='redirect'),
    url(r'^user/(?P<username>[^/]+)/$', 'user', name='user'),
    url(r'^users/$', 'users', name='users'),
)
