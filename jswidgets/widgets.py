from django import forms
from django.core.urlresolvers import reverse
from django.template import loader, Context
from django.utils.safestring import mark_safe
from .tools import idstring_to_list, idlist_to_models, get_display_field
from django.utils import simplejson as sj

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

        visible = super(SingleModelSelect, self).render(name+"_visible", self.visible_value(value), new_attrs)
        hidden_attrs = attrs.copy()
        hidden_attrs['type'] = 'hidden'
        hidden = super(SingleModelSelect, self).render(name, value, hidden_attrs)
        return visible + hidden

    def visible_value(self, value):
        if value:
            return self.model.objects.get(pk=int(value))
        else:
            return ""

    def get_css_class(self):
        return "jswidget-singleselect"

class MultiModelSelect(SingleModelSelect):

    def __init__(self, model, *args, **kwargs):
        self.list_item_template = "jswidgets/multimodelselect/list_item.js.tmpl"
        self.dropdown_item_template = None

        for my_kwarg in ("list_item_template", "dropdown_item_template"):
            if my_kwarg in kwargs:
                setattr(self, my_kwarg, kwargs.pop(my_kwarg))

        super(MultiModelSelect, self).__init__(model, *args, **kwargs)

    def render(self, name, value, attrs=None):
        if not attrs or 'id' not in attrs:
            raise Exception("Cannot instantiate MultiModelSelect without an id")
        html = []
        html.append(super(MultiModelSelect, self).render(name, value, attrs))
        existing_data = ""
        if value:
            models = idlist_to_models(idstring_to_list(value), self.model)
            display_field = get_display_field(self.model)
            field_data = [ { 'label' : getattr(model, display_field),
                             'id' : model.id,
                             } for model in models ]
            existing_data = "data-existing-data=%s"  % sj.dumps(field_data)
        html.append('<ul class="itemlist" id="%s_itemlist" %s></ul>' % (attrs['id'], existing_data))

        # js templates
        js_tmpl = loader.get_template(self.list_item_template)
        html.append(
                '<script type="text/template" id="%s_list_item_template">%s</script>'
                %(attrs['id'], js_tmpl.render(empty))
        )

        if self.dropdown_item_template:
            js_tmpl = loader.get_template(self.dropdown_item_template)
            html.append(
                    '<script type="text/template" id="%s_dropdown_item_template">%s</script>'
                    %(attrs['id'], js_tmpl.render(empty))
            )

        return mark_safe(u'\n'.join(html))

    def visible_value(self, value):
        return ""


    def get_css_class(self):
        return "jswidget-multiselect"

