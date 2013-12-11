import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from guardian.forms import UserObjectPermissionsForm, GroupObjectPermissionsForm
from guardian.mixins import LoginRequiredMixin
from guardian.shortcuts import get_perms, get_users_with_perms, get_groups_with_perms, get_objects_for_user, assign_perm
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
            assign_perm('view_node', request.user, node.get_nodeobject())
            if pk == 'add':
                return redirect('xdoc:edit', node.pk)

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
        nodes = get_objects_for_user(request.user, 'xdoc.view_node')
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


class PermissionsEditUser(LoginRequiredMixin, View):

    form = UserObjectPermissionsForm
    user_or_group_class = User

    def _get_context(self, request, pk, user):
        node = get_object_or_404(Node, pk=pk)
        user_or_group = get_object_or_404(self.user_or_group_class, pk=user)
        form = self.form(user_or_group, node, request.POST or None)
        c = {'form': form, 'request': request, 'node': node}
        return c

    def get(self, request, pk, user):
        c = self._get_context(request, pk, user)
        return render(request, 'xdoc/permissions_edit.html', c)

    def post(self, request, pk, user):
        c = self._get_context(request, pk, user)
        if c['form'].is_valid():
            c['form'].save_obj_perms()
            c['message'] = 'save successful'
        return render(request, 'xdoc/permissions_edit.html', c)


class PermissionsEditGroup(PermissionsEditUser):

    form = GroupObjectPermissionsForm
    user_or_group_class = Group


@login_required
def permissions_add(request, pk):
    if request.method == "POST":
        if 'username' in request.POST:
            try:
                user = User.objects.get(username=request.POST['username'])
                return redirect('xdoc:permissions_edit', pk=pk, user=user.pk)
            except ObjectDoesNotExist:
                pass
        if 'groupname' in request.POST:
            try:
                group = Group.objects.get(name=request.POST['groupname'])
                return redirect('xdoc:permissions_edit_group', pk=pk, user=group.pk)
            except ObjectDoesNotExist:
                pass
    return redirect('xdoc:permissions', pk=pk)
