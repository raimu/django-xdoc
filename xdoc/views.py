from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import viewsets
from xdoc.models import Node
from xdoc.serializers import NodeSerializer


@login_required
def main(request):
    return render(request, "xdoc/main.html")


class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer