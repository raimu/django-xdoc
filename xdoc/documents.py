import datetime
import mongoengine
from mongoengine import signals

mongoengine.connect('xdoc')


class Node(mongoengine.Document):
    name = mongoengine.StringField(required=False)
    path = mongoengine.StringField()
    date_modified = mongoengine.DateTimeField(default=datetime.datetime.now)
    parent = mongoengine.ReferenceField('self')

    meta = {'allow_inheritance': True}

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        if isinstance(document, Node):
            document.path = '/' + '/'.join(document._get_path())

    def _get_path(self):
        if self.parent == None:
            return [unicode(self.id)]
        return self.parent._get_path() + [unicode(self.id)]


class FolderNode(Node):
    pass


signals.pre_save.connect(Node.pre_save)
