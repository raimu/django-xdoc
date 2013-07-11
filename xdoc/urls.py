# coding=utf-8
from django.conf.urls import patterns, include, url
from xdoc import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^folder.json$', views.tree, name='tree'),
    url(r'^table.json$', views.table, name='table'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^edit/(?P<pk>[\w\d]+)/$', views.edit, name='edit'),
    url(r'^edit/(?P<pk>[\w\d]+)/(?P<node_class>.+)/$', views.edit, name='edit'),
    url(r'^show/(?P<pk>[\w\d]+)/$', views.show, name='show'),
)