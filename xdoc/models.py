from django.db import models
from django.forms import ModelForm


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
        return NODE_MAP[self.filetype]['thumbnail']

    @property
    def filetype(self):
        if self._filetype == '':
            return self.__class__.__name__
        return self._filetype

    @property
    def form(self):
        form = NODE_MAP[self.filetype]['form']
        return form

    def get_fileobject(self):
        return NODE_MAP[self.filetype]['node'].objects.get(pk=self.pk)

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


#TODO: Move to settings
NODE_MAP = {
    'Node': {
        'node': Node,
        'form': NodeForm,
        'thumbnail': '/static/xdoc/lib/icons/places/folder.png'
    },
    'Document': {
        'node': Document,
        'form': DocumentForm,
        'thumbnail': '/static/xdoc/lib/icons/mimetypes/text-plain.png'

    },
}