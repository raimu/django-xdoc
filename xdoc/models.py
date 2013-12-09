from django.conf import settings
from django.db import models
from django.forms import ModelForm
from django.utils.importlib import import_module


class Node(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    _filetype = models.CharField(max_length=100, blank=True, editable=False)
    path_id = models.TextField(blank=True, null=True, editable=False)

    @property
    def path(self):
        if self.parent is None:
            return [self]
        return self.parent.path + [self]

    @property
    def thumbnail_url(self):
        return self._get_settings('thumbnail')

    @property
    def filetype(self):
        if self._filetype == '':
            return self.__class__.__name__
        return self._filetype

    @property
    def has_children(self):
        if Node.objects.filter(parent=self).count() > 0:
            return True
        return False

    @property
    def form(self):
        return import_class(self._get_settings('form'))

    def get_template(self, name, default=None):
        node_setting = settings.XDOC_NODE_MAP[self.filetype]
        if name in node_setting:
            if 'template' in node_setting[name]:
                return node_setting[name]['template']
        return default

    def get_fileobject(self):
        return import_class(self._get_settings('node')).objects.get(pk=self.pk)

    def get_nodeobject(self):
        return Node.objects.get(pk=self.pk)

    @staticmethod
    def create_new_fileobject(name):
        return import_class(settings.XDOC_NODE_MAP[name]['node'])()

    def _get_settings(self, name):
        return settings.XDOC_NODE_MAP[self.filetype][name]

    def save(self, *args, **kwargs):
        super(Node, self).save(*args, **kwargs)
        self._filetype = self.filetype
        self.path_id = '/' + '/'.join([str(i.pk) for i in self.path])
        super(Node, self).save()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        permissions = (
            ('view_node', 'can view node'),
        )


class Document(Node):
    content = models.TextField()


class NodeForm(ModelForm):
    class Meta:
        model = Node


class DocumentForm(ModelForm):
    class Meta:
        model = Document


def import_class(name):
    name = name.split('.')
    module = import_module('.'.join(name[:-1]))
    return getattr(module, name[-1])