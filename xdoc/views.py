# Create your views here.
import json
from bson import ObjectId
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.web import JsonLexer
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
    html = u'''<a class="btn iframe" href="%s"><i class="icon-%s"></i></a>'''
    data = []
    for node in result[start:end]:
        rows = [unicode(node[col]) for col in columns]
        links = html % (reverse('edit', args=[unicode(node.pk)]), u'edit')
        links += html % (reverse('show', args=[unicode(node.pk)]), u'eye-open')
        rows.append(links)
        data.append(rows)

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


def show(request, pk):
    data = json.loads(Node.objects.get(id=ObjectId(pk)).to_json())
    code = json.dumps(data, indent=4)
    return render(request, 'xdoc/show.html', {
        'data': highlight(code, JsonLexer(), HtmlFormatter()),
    })