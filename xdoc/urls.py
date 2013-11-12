from django.conf.urls import patterns, include, url
from rest_framework import routers
from xdoc import views

router = routers.DefaultRouter()
router.register(r'node', views.NodeViewSet)

urlpatterns = patterns('xdoc.views',
    url(r'^$', 'main', name='main'),
    url(r'^config/', 'config', name='config'),
    url(r'^(?P<pk>add)/(?P<node_name>.+)/', 'edit', name='add'),
    url(r'^edit/(?P<pk>\d+)/', 'edit', name='edit'),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
)
