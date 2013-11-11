from django.contrib import admin
from xdoc.models import Node, Document


class NodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'filetype', 'path', 'created_at', 'updated_at')
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name']


admin.site.register(Node, NodeAdmin)
admin.site.register(Document, NodeAdmin)
