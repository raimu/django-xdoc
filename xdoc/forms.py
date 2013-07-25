from documents import Folder, Text, Link
from mongodbforms import DocumentForm
from django.forms import widgets

from xdoc.widgets import ckEditor


class TextForm(DocumentForm):

    class Meta:
        document = Text
        fields = ('name', 'content', 'parent', )

        widgets = {
            'name': widgets.TextInput({'class': 'input-xxlarge'}),
            'content': ckEditor(),
            'parent': widgets.TextInput(),
        }


class FolderForm(DocumentForm):

    class Meta:
        document = Folder
        fields = ('name', 'parent', )

        widgets = {
            'name': widgets.TextInput({'class': 'input-xxlarge'}),
            'parent': widgets.TextInput(),
        }


class LinkForm(DocumentForm):

    class Meta:
        document = Link
        fields = ('name', 'url', 'parent', )

        widgets = {
            'name': widgets.TextInput({'class': 'input-xxlarge'}),
            'url': widgets.TextInput({'class': 'input-xxlarge'}),
            'parent': widgets.TextInput(),
        }