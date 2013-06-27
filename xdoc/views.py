# Create your views here.
import json
from bson import ObjectId
from django.http import HttpResponse
from django.shortcuts import render
from xdoc.documents import Node


def index(request):
    return render(request, 'xdoc/index.html')


def tree(request):
    if request.GET['root'] == 'source':
        parent = None
    else:
        parent = ObjectId(request.GET['root'])
    tree = []
    for node in Node.objects(parent=parent):
        children = Node.objects(path__startswith=node.path).count() -1
        current = {
            'text': '%s (%s)' %(node.name, children),
            'expanded': False,
            'id': str(node.id),
            'hasChildren': False,
            'classes': 'folder',
        }
        if children >= 1:  #  has children?
            current['hasChildren'] = True
        tree.append(current)
    return HttpResponse(json.dumps(tree))


def table(request):
    columns = ['id', 'name', 'date_modified']
    order_column = columns[int(request.GET['iSortCol_0'])]
    start = int(request.GET['iDisplayStart'])
    end = int(request.GET['iDisplayLength']) + start

    result = Node.objects.all()

    if request.GET['sSearch'] != '':
        result = result.filter(name__icontains=request.GET['sSearch'])
    if request.GET['sSortDir_0'] == 'asc':
        result = result.order_by('+%s' % order_column)
    if request.GET['sSortDir_0'] == 'desc':
        result = result.order_by('-%s' % order_column)

    # convert result-object in a list
    data = [[unicode(node[i]) for i in columns] for node in result[start:end]]

    return HttpResponse(json.dumps({
        'sEcho': request.GET['sEcho'],
        'iTotalRecords': Node.objects.count(),
        'iTotalDisplayRecords': result.count(),
        'aaData': data,
        }))
