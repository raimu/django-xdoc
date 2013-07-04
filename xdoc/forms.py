from documents import TextDocument, FolderNode
from mongodbforms import DocumentForm


class TextForm(DocumentForm):

    class Meta:
        document = TextDocument
        fields = ('name', 'content', 'parent')


class FolderForm(DocumentForm):

    class Meta:
        document = FolderNode
        fields = ('name', 'parent')
