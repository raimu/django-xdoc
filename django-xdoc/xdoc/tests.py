from django.test import TestCase
from xdoc.models import Node


class NodeMethodTests(TestCase):

    def test_node_thumbnail_url(self):
        node = Node(name="foo.txt")
        assert 'folder.png' in node.thumbnail_url