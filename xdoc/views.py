# Create your views here.
import json
from django.http import HttpResponse
from django.shortcuts import render
from xdoc.documents import FolderNode


def index(request):
    return render(request, 'xdoc/index.html')


def folder(request):
    parent = None
    tree = []
    for node in FolderNode.objects(parent=parent):
        current = {
            'text': node.name,
            'expanded': False,
            'id': str(node.id),
            'hasChildren': False,
            'classes': 'folder',
        }
        if len(FolderNode.objects(parent=node.id)) >= 1:  #  has children?
            current['hasChildren'] = True
        tree.append(current)
    return HttpResponse(json.dumps(tree))

