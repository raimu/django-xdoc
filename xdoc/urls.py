from django.conf.urls import patterns, include, url
from rest_framework import routers
from xdoc import views


urlpatterns = patterns('xdoc.views',
    url(r'^$', 'main', name='main'),
    url(r'^(?P<pk>add)/(?P<node_name>.+)/', 'edit', name='add'),
    url(r'^edit/(?P<pk>\d+)/', 'edit', name='edit'),
    url(r'^api/config/', 'config', name='config'),
    url(r'^api/node/$', views.NodeList.as_view(), name="node_list"),
    url(r'^api/node/(?P<pk>[0-9]+)$',  views.NodeDetail.as_view(), name="node_detail"),
)
