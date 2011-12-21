from django import forms
from django.core.urlresolvers import reverse
from django.template import loader, Context
from django.utils.safestring import mark_safe

empty = Context({})


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
        return "jswidget-singleselect"

class MultiModelSelect(SingleModelSelect):

    def __init__(self, model, *args, **kwargs):
        self.list_item_template = "jswidgets/multimodelselect/list_item.js.tmpl"
        self.dropdown_template = "jswidgets/multimodelselect/dropdown_item.js.tmpl"
        for my_kwarg in ("list_item_template", "dropdown_item_template"):
            if my_kwarg in kwargs:
                setattr(self, my_kwarg, kwargs.pop(my_kwarg))

        super(MultiModelSelect, self).__init__(model, *args, **kwargs)

    def render(self, name, value, attrs=None):
        if not attrs or 'id' not in attrs:
            raise Exception("Cannot instantiate MultiModelSelect without an id")
        html = []
        html.append(super(MultiModelSelect, self).render(name, value, attrs))
        html.append('<ul class="itemlist" id="%s_itemlist"></ul>' % attrs['id'])

        # js templates
        js_tmpl = loader.get_template(self.list_item_template)
        html.append(
                '<script type="text/template" id="%s_list_item_template">%s</script>'
                %(attrs['id'], js_tmpl.render(empty))
        )

        js_tmpl = loader.get_template(self.dropdown_template)
        html.append(
                '<script type="text/template" id="%s_dropdown_item_template">%s</script>'
                %(attrs['id'], js_tmpl.render(empty))
        )

        return mark_safe(u'\n'.join(html))

    def get_css_class(self):
        return "jswidget-multiselect"

