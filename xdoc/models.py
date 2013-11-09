from django.db import models


class Node(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def path(self):
        return "/path/to/node"

    @property
    def thumbnail_url(self):
        return "/static/xdoc/lib/icons/places/folder.png"

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Document(Node):
    content = models.TextField()
