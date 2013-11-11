from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from xdoc.models import Node, Document, NodeForm


class NodeMethodTests(TestCase):

    def test_document_thumbnail_url(self):
        Document(name='foo.txt').save()
        node = Node.objects.get(name='foo.txt')
        self.assertIn('text', node.thumbnail_url)

    def test_thumbnail_url_before_save(self):
        node = Node(name='foo')
        self.assertIn('folder', node.thumbnail_url)

    def test_filetype(self):
        document = Document(name='foo.txt')
        document.save()
        self.assertEqual('Document', document.filetype)

    def test_document_get_fileobject(self):
        Document(name='foo.txt').save()
        node = Node.objects.get(name='foo.txt')
        self.assertIsInstance(node.get_fileobject(), Document)
        self.assertEqual('foo.txt', node.get_fileobject().name)

    def test_change_filetype_only_on_create(self):
        Document(name='foo.txt').save()
        node = Node.objects.get(name='foo.txt')
        node.save()
        self.assertIsInstance(node.get_fileobject(), Document)

    def test_path(self):
        foo = Node(name='foo')
        bar = Node(name='bar', parent=foo)
        baz = Document(name='baz.txt', parent=bar)
        self.assertEqual('foo/bar/baz.txt', '/'.join(baz.path))

    def test_form(self):
        node = Node(name='foo')
        self.assertIsInstance(node.form(), NodeForm)


class ViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='secret')
        self.node = Node(name='foo')
        self.node.save()

    def login(self):
        self.client.login(username='test', password='secret')

    def test_main_without_login(self):
        response = self.client.get(reverse('xdoc:main'))
        self.assertEquals(302, response.status_code)

    def test_main_with_login(self):
        self.login()
        response = self.client.get(reverse('xdoc:main'))
        self.assertEquals(200, response.status_code)
        self.assertInHTML('<div ng-view/>', response.content)

    def test_edit(self):
        self.login()
        response = self.client.get(
            reverse('xdoc:edit', kwargs={'pk': self.node.pk}))
        self.assertIn('value="foo"', response.content)

    def test_edit_with_POST(self):
        self.login()
        response = self.client.post(
            reverse('xdoc:edit', kwargs={'pk': self.node.pk}),
            data={'name': 'bar.txt'})
        self.assertIn('save successful', response.content)
        self.assertEqual('bar.txt', Node.objects.get().name)