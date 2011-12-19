from django import forms
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe


class SingleModelSelect(forms.TextInput):
    """ 
    Use this to select a single instance of a model
    with too many to have a simple select field.
    Must be used on a field with a queryset variable
    """

    def __init__(self, model, *args, **kwargs):
        self.model = model
        super(SingleModelSelect, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        new_attrs = attrs.copy()
        css = new_attrs.get('class', '')
        if css:
            css += ' '
        css += self.get_css_class()
        new_attrs['class'] = css
        new_attrs['data-sourceurl'] = reverse(
            "aw_search_%s_%s" % (self.model._meta.app_label, 
                                 self.model.__name__)
            )
        new_attrs['data-target-id'] = new_attrs['id']
        new_attrs['id'] = new_attrs['id'] + '_visible'

        visible = super(SingleModelSelect, self).render(name+"_visible", value, new_attrs)
        hidden_attrs = attrs.copy()
        hidden_attrs['type'] = 'hidden'
        hidden = super(SingleModelSelect, self).render(name, value, hidden_attrs)
        return visible + hidden

    def get_css_class(self):
        return "ajax_widget_singleselect ajax_widget"

class MultiModelSelect(SingleModelSelect):
    def render(self, name, value, attrs=None):
        if not attrs or 'id' not in attrs:
            raise Exception("Cannot instantiate MultiModelSelect without an id")
        html = [super(MultiModelSelect, self).render(name, value, attrs)]
        html.append('<ul class="itemlist" id="%s_itemlist"></ul>' % attrs['id'])
        return mark_safe(u'\n'.join(html))

    def get_css_class(self):
        return "ajax_widget_multiselect ajax_widget"

