# Create your views here.
import json
from bson import ObjectId
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
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


def edit(request, pk=None, node_class=None):
    mapping = settings.XDOC_DOCUMENT_MAPPING
    if pk is None or pk == 'None':
        if node_class is None:
            return render(request, 'xdoc/edit_choose_node.html', {
                'mapping': [[i, mapping[i]['label']] for i in mapping],
            })
        instance = mapping[node_class]['node']()
        form_obj = mapping[node_class]['form']
        url = reverse('edit', args=[instance.pk, node_class])
    else:
        instance = Node.objects.get(id=ObjectId(pk))
        form_obj = mapping[instance._cls]['form']
        url = reverse('edit', args=[instance.pk])

    if request.method == 'POST':
        form = form_obj(request.POST, instance=instance)
        if form.is_valid():
            instance = form.instance
            instance.save().save()  # todo: build path after save
            return HttpResponseRedirect(reverse('edit', args=[instance.pk]))
    else:
        form = form_obj(instance=instance)

    return render(request, 'xdoc/edit.html', {
        'form': form,
        'url': url,
    })