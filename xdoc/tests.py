import json
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

    def test_has_children(self):
        node = Node(name='foo')
        node.save()
        document = Document(name='bar.txt', parent=node)
        document.save()
        self.assertTrue(node.has_children)
        self.assertFalse(document.has_children)

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
        self.assertEqual('foo/bar/baz.txt',
                         '/'.join([i.name for i in baz.path]))

    def test_form(self):
        node = Node(name='foo')
        self.assertIsInstance(node.form(), NodeForm)


class ViewTestWithoutLogin(TestCase):

    def test_main_without_login(self):
        response = self.client.get(reverse('xdoc:main'))
        self.assertEquals(302, response.status_code)


class ViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='secret')
        self.client.login(username='test', password='secret')
        self.node = Node(name='foo')
        self.node.save()

    def test_main(self):
        response = self.client.get(reverse('xdoc:main'))
        self.assertEquals(200, response.status_code)
        self.assertInHTML('<div ng-view/>', response.content)

    def test_edit(self):
        response = self.client.get(
            reverse('xdoc:edit', kwargs={'pk': self.node.pk}))
        self.assertIn('value="foo"', response.content)

    def test_edit_with_POST(self):
        response = self.client.post(
            reverse('xdoc:edit', kwargs={'pk': self.node.pk}),
            data={'name': 'bar.txt'})
        self.assertIn('save successful', response.content)
        self.assertEqual('bar.txt', Node.objects.get().name)

    def test_add(self):
        response = self.client.get(
            reverse('xdoc:add', kwargs={'pk': 'add', 'node_name': 'Node'}))
        self.assertIn('value=""', response.content)  # empty field

    def test_add_with_POST(self):
        response = self.client.post(
            reverse('xdoc:add', kwargs={'pk': 'add', 'node_name': 'Node'}),
            data={'name': 'bar.txt'})
        self.assertIn('save successful', response.content)
        self.assertEqual(2, Node.objects.all().count())  # insert row

    def test_node_detail(self):
        response = self.client.get(
            reverse('xdoc:node_detail', kwargs={'pk': self.node.pk}))
        self.assertDictContainsSubset({'name': 'foo'},
                                      json.loads(response.content))

    def test_siteconfig(self):
        response = self.client.get(reverse('xdoc:config'))
        data = json.loads(response.content)
        self.assertDictContainsSubset({'username': 'test'}, data)
        self.assertIn('node_map', data)

    def test_node_list(self):
        response = self.client.get(reverse('xdoc:node_list'))
        data = json.loads(response.content)
        self.assertDictContainsSubset({'name': 'foo'}, data['results'][0])

    def test_node_list_with_query(self):
        Document(name='bar.txt').save()
        response = self.client.get(reverse('xdoc:node_list'), {'q': 'foo'})
        self.assertIn('foo', response.content)
        self.assertNotIn('bar', response.content)
        response = self.client.get(reverse('xdoc:node_list'), {'q': 'bar'})
        self.assertIn('bar', response.content)

    def test_node_list_with_parent_node(self):
        Document(name='bar.txt', parent=self.node).save()

        # without parent-parameter
        response = self.client.get(reverse('xdoc:node_list'))
        self.assertNotIn('bar', response.content)

        # with parent-parameter
        response = self.client.get(reverse('xdoc:node_list'), {
            'parent_node': self.node.pk})
        self.assertIn('bar', response.content)

    def test_node_list_parent_path(self):
        Document(name='bar.txt', parent=self.node).save()
        response = self.client.get(reverse('xdoc:node_list'), {
            'parent_node': self.node.pk})
        data = json.loads(response.content)
        self.assertEqual([['foo', self.node.id]], data['path'])
