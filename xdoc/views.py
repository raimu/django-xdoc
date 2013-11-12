import json
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from xdoc.models import Node
from xdoc.serializers import NodeSerializer


@login_required
def main(request):
    return render(request, "xdoc/main.html")


class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer


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

    c = {'form': form, 'request': request, 'message': message}
    c.update(csrf(request))
    return render(request, "xdoc/edit.html", c)


def config(request):
    siteconfig = {
        'node_map': [key for key in settings.XDOC_NODE_MAP],
        'username': request.user.username,
    }
    return HttpResponse(json.dumps(siteconfig))