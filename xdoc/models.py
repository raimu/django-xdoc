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

    @property
    def path(self):
        if self.parent is None:
            return [self.name]
        return self.parent.path + [self.name]

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

    def get_fileobject(self):
        return import_class(self._get_settings('node')).objects.get(pk=self.pk)

    @staticmethod
    def create_new_fileobject(name):
        return import_class(settings.XDOC_NODE_MAP[name]['node'])()

    def _get_settings(self, name):
        return settings.XDOC_NODE_MAP[self.filetype][name]

    def save(self, *args, **kwargs):
        self._filetype = self.filetype
        super(Node, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


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