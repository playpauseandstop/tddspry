from django.conf.urls.defaults import *


urlpatterns = patterns('testproject.testapp.views',
    url(r'^$', 'index', name='index'),
    url(r'^user/(?P<username>[^/]+)/$', 'user_info', name='user_info'),
    url(r'^users/$', 'user_list', name='user_list'),
)
