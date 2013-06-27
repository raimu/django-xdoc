# Create your views here.
import json
from bson import ObjectId
from django.http import HttpResponse
from django.shortcuts import render
from xdoc.documents import Node, FolderNode


def index(request):
    return render(request, 'xdoc/index.html')


def tree(request):
    if request.GET['root'] == 'source':
        parent = None
    else:
        parent = ObjectId(request.GET['root'])
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


def table(request):
    columns = ['id', 'name', 'date_modified']
    result = Node.objects
    if request.GET['sSearch'] != '':
        result = result.filter(name__icontains=request.GET['sSearch'])
    if request.GET['sSortDir_0'] == 'asc':
        if request.GET['iSortCol_0'] == '0':
            result = result.order_by('+id')
        if request.GET['iSortCol_0'] == '1':
            result = result.order_by('+name')
    if request.GET['sSortDir_0'] == 'desc':
        if request.GET['iSortCol_0'] == '0':
            result = result.order_by('-id')
        if request.GET['iSortCol_0'] == '1':
            result = result.order_by('-name')
    data = {
        'sEcho': request.GET['sEcho'],
        'iTotalRecords': Node.objects.count(),
        'iTotalDisplayRecords': result.count(),
        'aaData': [],
        }
    start = int(request.GET['iDisplayStart'])
    end = int(request.GET['iDisplayLength']) + start
    for node in result[start:end]:
        data['aaData'].append([unicode(node[i]) for i in columns])
    return HttpResponse(json.dumps(data))
