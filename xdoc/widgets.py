from django.forms import widgets, forms


class ckEditor(widgets.Textarea):

    @property
    def media(self):
        return forms.Media(js=["xdoc/lib/ckeditor/ckeditor.js"])

    def __init__(self, attrs=None):
        default_attrs = {'class': 'ckeditor'}
        if attrs:
            default_attrs.update(attrs)
        super(widgets.Textarea, self).__init__(default_attrs)

