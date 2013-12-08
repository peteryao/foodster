from django.conf.urls import patterns, include, url

urlpatterns = patterns('core.views',
    url('^$', 'index', name='index'),
    url('^restraunt/(?P<restraunt_id>\d+)/$', 'restraunt', name='restraunt'),
    url('^menu/(?P<restraunt_id>\w+)/$', 'menu', name='menu'),
    url('^receipt/(?P<restraunt_id>\w+)/$', 'receipt', name='receipt'),
)