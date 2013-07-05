from documents import TextDocument, FolderNode
from mongodbforms import DocumentForm
from django.forms import widgets


class TextForm(DocumentForm):

    class Meta:
        document = TextDocument
        fields = ('name', 'content', 'parent')

        widgets = {
            'name': widgets.TextInput(),
            'content': widgets.Textarea({'class': 'ckeditor'}),
        }


class FolderForm(DocumentForm):

    class Meta:
        document = FolderNode
        fields = ('name', 'parent')

        widgets = {
            'name': widgets.TextInput(),
        }
