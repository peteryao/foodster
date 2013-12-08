from django.conf.urls import patterns, include, url

urlpatterns = patterns('core.views',
    url(r'^$', 'index', name='index'),
    url(r'^restraunt/(?P<restraunt_id>\d+)/$', 'restraunt', name='restraunt'),
    url(r'^menu/(?P<restraunt_id>\w+)/$', 'menu', name='menu'),
    url(r'^receipt/(?P<restraunt_id>\w+)/$', 'receipt', name='receipt'),
    url(r'^store/$', 'receipt', name='receipt'),
    url(r'^paypay_payment/$', 'ebay', name='ebay'),

    url(r'^user_info/', 'user_info', name='user_info'),
)

