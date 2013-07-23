from documents import Folder, Text, Link
from mongodbforms import DocumentForm
from django.forms import widgets

from xdoc.widgets import ckEditor


class TextForm(DocumentForm):

    class Meta:
        document = Text
        fields = ('name', 'content', )

        widgets = {
            'name': widgets.TextInput({'class': 'input-xxlarge'}),
            'content': ckEditor(),
        }


class FolderForm(DocumentForm):

    class Meta:
        document = Folder
        fields = ('name', )

        widgets = {
            'name': widgets.TextInput({'class': 'input-xxlarge'}),
        }


class LinkForm(DocumentForm):

    class Meta:
        document = Link
        fields = ('name', 'url', )

        widgets = {
            'name': widgets.TextInput({'class': 'input-xxlarge'}),
            'url': widgets.TextInput({'class': 'input-xxlarge'}),
        }