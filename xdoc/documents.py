import datetime
import mongoengine

mongoengine.connect('xdoc')


class Node(mongoengine.Document):
    name = mongoengine.StringField(required=False)
    date_modified = mongoengine.DateTimeField(default=datetime.datetime.now)

    meta = {'allow_inheritance': True}


class FolderNode(Node):
    parent = mongoengine.ReferenceField('FolderNode')
