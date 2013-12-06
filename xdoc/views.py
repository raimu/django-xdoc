import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from guardian.forms import UserObjectPermissionsForm
from guardian.shortcuts import get_perms, get_users_with_perms, get_groups_with_perms
from rest_framework.response import Response
from rest_framework.views import APIView
from xdoc.models import Node
from xdoc.serializers import NodeSerializer


@login_required
def main(request):
    return render(request, "xdoc/main.html")


@login_required
def edit(request, pk, node_name=None):
    message = []
    if pk == 'add' and node_name is not None:
        node = Node.create_new_fileobject(node_name)
    else:
        node = get_object_or_404(Node, pk=pk).get_fileobject()

    form = node.form(instance=node)
    if request.method == 'POST':
        form = node.form(request.POST, request.FILES, instance=node)
        if form.is_valid():
            message.append('save successful')
            form.save()

    c = {'form': form, 'request': request, 'message': message, 'node': node}
    c.update(csrf(request))
    template = node.get_template('edit', default="xdoc/edit.html")
    return render(request, template, c)


def config(request):
    siteconfig = {
        'node_map': settings.XDOC_NODE_MAP,
        'username': request.user.username,
    }
    return HttpResponse(json.dumps(siteconfig))


class NodeList(APIView):

    def get_param(self, name, default):
        if name in self.request.GET:
            return self.request.GET[name]
        return default

    def get(self, request, format=None):
        self.request = request
        nodes = Node.objects.all()
        result = {
            'parent_node': int(self.get_param('parent_node', default=0)),
            'start': int(self.get_param('start', default=0)),
            'paginate': int(self.get_param('paginate', default=10)),
            'q': self.get_param('q', default=''),
        }

        if result['parent_node'] == 0:
            result['parent_node'] = None
            result['path'] = None
        else:
            parent = get_object_or_404(Node, pk=result['parent_node'])
            result['path'] = [[i.name, i.id] for i in parent.path]
            nodes = nodes.filter(path_id__startswith=parent.path_id)

        if result['q'] == '':
            nodes = nodes.filter(parent=result['parent_node'])
        else:
            nodes = nodes.filter(name__contains=result['q'])

        end = result['paginate'] + result['start']
        serializer = NodeSerializer(nodes[result['start']:end], many=True)
        result['results'] = serializer.data
        result['count'] = nodes.count()
        return Response(result)


class NodeDetail(APIView):

    def get(self, request, pk, format=None):
        node = get_object_or_404(Node, pk=pk)
        serializer = NodeSerializer(node)
        return Response(serializer.data)


@login_required
def permissions(request, pk):
    node = get_object_or_404(Node, pk=pk)
    users = get_users_with_perms(node, with_group_users=False)
    users = [[i, get_perms(i, node)] for i in users]
    groups = [[i, get_perms(i, node)] for i in get_groups_with_perms(node)]
    c = {'users': users, 'groups': groups, 'node': node}
    c.update(csrf(request))
    return render(request, 'xdoc/permissions.html', c)


@login_required
def permissions_edit(request, pk, user):
    message = []
    node = get_object_or_404(Node, pk=pk)
    user = get_object_or_404(User, pk=user)
    form = UserObjectPermissionsForm(user, node, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save_obj_perms()
        message.append('save successful')
    c = {'form': form, 'request': request, 'node': node, 'message': message}
    return render(request, 'xdoc/permissions_edit.html', c)


@login_required
def permissions_add(request, pk):
    if request.method == "POST" and 'username' in request.POST:
        try:
            user = User.objects.get(username=request.POST['username'])
            return redirect('xdoc:permissions_edit', pk=pk, user=user.pk)
        except ObjectDoesNotExist:
            pass
    return redirect('xdoc:permissions', pk=pk)
