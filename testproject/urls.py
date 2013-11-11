from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^xdoc/', include('xdoc.urls', namespace='xdoc')),

    (r'^accounts/login/$', 'django.contrib.auth.views.login', {
        'template_name': 'xdoc/login.html'}),
    ('logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
)
