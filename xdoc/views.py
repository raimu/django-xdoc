import json
from bson import ObjectId
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.web import JsonLexer
from xdoc.documents import Node, Folder


@login_required
def index(request):
    return render(request, 'xdoc/index.html')


@login_required
def tree(request):
    if request.GET['id'] == '0':
        parent = None
    else:
        parent = ObjectId(request.GET['id'])
    tree = []
    for node in Folder.objects(parent=parent):
        children = Node.objects(_id_path__startswith=node._id_path).count() - 1
        current = {
            'attr': {'id': str(node.id), 'rel': 'folder',
                     'title': unicode(node.name)},
            'data': unicode(node.name),
        }
        if children >= 1:  #  has children?
            current['state'] = 'closed'
        tree.append(current)
    return HttpResponse(json.dumps(tree))


@login_required
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
    tmpl = u'''<a class="btn iframe" href="%s"><i class="icon-%s"></i></a>'''
    data = []
    for node in result[start:end]:
        rows = [unicode(node[col]) for col in columns]
        links = tmpl % (reverse('edit', args=[unicode(node.pk)]), u'edit')
        links += tmpl % (reverse('show', args=[unicode(node.pk)]), u'leaf')
        if hasattr(node, 'url'):
            links += tmpl % (node.url, u'road')
            links += u'''<a class="btn" target="_blank" href="%s">
            <i class="icon-%s"></i></a>''' % (node.url, u'globe')
        rows.append(links)
        data.append(rows)

    return HttpResponse(json.dumps({
        'sEcho': request.GET['sEcho'],
        'iTotalRecords': Node.objects.count(),
        'iTotalDisplayRecords': result.count(),
        'aaData': data,
        }))


@login_required
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

    c = {'form': form, 'url': url, }
    if instance.pk:
        if instance.parent:
            c['selected_parent'] = instance.parent.pk
        c['initially_open'] = json.dumps(instance._id_path.split('/')[1:-2])
    return render(request, 'xdoc/edit.html', c)


@login_required
def show(request, pk):
    data = json.loads(Node.objects.get(id=ObjectId(pk)).to_json())
    code = json.dumps(data, indent=4)
    return render(request, 'xdoc/show.html', {
        'data': highlight(code, JsonLexer(), HtmlFormatter()),
    })


def xdoc_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))