from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
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
def edit(request, pk):
    message = []
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