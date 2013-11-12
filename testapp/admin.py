from django.contrib import admin
from testapp.models import BusinessCard, Picto
from xdoc.admin import NodeAdmin


admin.site.register(BusinessCard, NodeAdmin)
admin.site.register(Picto)
