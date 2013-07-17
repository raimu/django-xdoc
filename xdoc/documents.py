import datetime
import mongoengine
from mongoengine import signals


class Node(mongoengine.Document):

    name = mongoengine.StringField(required=False)
    date_modified = mongoengine.DateTimeField(default=datetime.datetime.now)
    parent = mongoengine.ReferenceField('Node')

    _id_path = mongoengine.StringField()

    meta = {
        'allow_inheritance': True,
        'indexes': ['name', '_id_path']
    }

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        if isinstance(document, Node):
            document._id_path = '/' + '/'.join(document._get_path())

    def _get_path(self):
        if self.parent == None:
            return [unicode(self.id)]
        return self.parent._get_path() + [unicode(self.id)]

    def __unicode__(self):
        return unicode(self.name)


class Folder(Node):
    pass


class Document(Node):
    pass


class Text(Document):

    content = mongoengine.StringField()


class Link(Document):

    url = mongoengine.URLField()


signals.pre_save.connect(Node.pre_save)
