import datetime
import mongoengine
from mongoengine import signals


class Node(mongoengine.Document):

    name = mongoengine.StringField(required=False)
    path = mongoengine.StringField()
    date_modified = mongoengine.DateTimeField(default=datetime.datetime.now)
    parent = mongoengine.ReferenceField('Node')

    meta = {'allow_inheritance': True}

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        if isinstance(document, Node):
            document.path = '/' + '/'.join(document._get_path())

    def _get_path(self):
        if self.parent == None:
            return [unicode(self.id)]
        return self.parent._get_path() + [unicode(self.id)]

    def __unicode__(self):
        return unicode(self.name)


class FolderNode(Node):
    pass


class Document(Node):
    pass


class TextDocument(Document):

    content = mongoengine.StringField()


signals.pre_save.connect(Node.pre_save)
