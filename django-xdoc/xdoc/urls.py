from django.conf.urls import patterns, include, url


urlpatterns = patterns('xdoc.views',
    url(r'^$', 'main'),
)
