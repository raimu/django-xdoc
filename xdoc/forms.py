from documents import TextDocument
from mongodbforms import DocumentForm


class TextForm(DocumentForm):

    class Meta:
        document = TextDocument
        fields = ('name', 'content', 'parent')
