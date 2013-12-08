from django.contrib import admin
from xdoc.models import Node, Document
from guardian.admin import GuardedModelAdmin


class NodeAdmin(GuardedModelAdmin):
    list_display = ('name', 'filetype', 'path', 'created_at', 'updated_at')
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name']


admin.site.register(Node, NodeAdmin)
admin.site.register(Document, NodeAdmin)
