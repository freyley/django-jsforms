from django import forms
from django.core.urlresolvers import reverse
from django.template import loader, Context
from django.utils.safestring import mark_safe
from .tools import idstring_to_list, idlist_to_models, get_display_field
from django.utils import simplejson as sj

import urllib

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
        return "jswidgets-singleselect"

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
            existing_data = "data-existing-data='%s'" % urllib.quote(sj.dumps(field_data))
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
        return "jswidgets-multiselect"



class ModelFormset(forms.TextInput):

    def __init__(self, form_class, *args, **kwargs):
        self.format = kwargs.pop('format', None)
        self.template = kwargs.pop('template', None)
        self.extra = kwargs.pop('extra', 0)
        if self.template:
            self.format = 'template'

        self.form_class = form_class
        super(ModelFormset, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        field_name = self._field.save_to or name
        mfs_factory = forms.models.modelformset_factory(
                self.form_class._meta.model,
                can_delete=True,
                extra=self.extra)

        try:
            dataset = getattr(self._field._form.instance, field_name).all()
            fs = mfs_factory(prefix="jswidgets-%s" % name, queryset=dataset)
        except ValueError:
            fs = mfs_factory(prefix="jswidgets-%s" % name, queryset=self.form_class._meta.model.objects.none())

        script_open = '<script type="text/template" class="jswidgets-formsetfield-template" data-name="%s">' % name
        add_button = '<a class="jswidgets-formsetfield-addform-%s" href="#">add form</a>' % name

        if self.format == 'ul':
            open_ul = '<ul class="jswidgets-formsetfield-form-%s">' % name
            r = "".join((
                    fs.management_form.as_ul(),
                    script_open,
                    open_ul,
                    fs.empty_form.as_ul(),
                    '</ul>',
                    '</script>',
                    ))
            for f in fs.forms:
                r += open_ul + f.as_ul() + "</ul>"
            r += add_button
            return r

        elif self.format == 'table':
            return '%s</tr><script type="text/template">%s</script>' % (fs.as_table(), fs.empty_form.as_table())
        elif self.format == 'p':
            return '%s<script class="jswidgets-formsetfield" type="text/template">%s</script>' % (fs.as_p(), fs.empty_form.as_p())
        elif self.format == 'template':
            # TODO
            return "a template"









class ImageFormset(forms.TextInput):

    def __init__(self, form, *args, **kwargs):
        self.form = form()
        super(ImageFormset, self).__init__(*args, **kwargs)


    def render(self, name, value, attrs=None):
        new_attrs = attrs.copy()

        css_class = self.get_css_class()
        css = new_attrs.get('class', '')
        if css:
            css += ' '
        css += css_class
        new_attrs['class'] = css

        new_attrs['type'] = 'hidden'
        hidden = super(ImageFormset, self).render(name, value, new_attrs)

        retval = '''
            <div class="%(css_class)s" id="%(css_class)s-%(name)s">
               %(hidden)s
               <ul class="%(css_class)s-images">put image data here</ul>
            <script type="text/template" class="%(css_class)s-newform">
                <form class="%(css_class)s-newform" action="%(action)s">
                %(form)s
                <input class="%(css_class)s" type="submit" value="save">
                </form>
            </script>
            <button>upload new image</button>
            </div>
        ''' % dict(css_class=css_class, name=name, hidden=hidden,
                    form=self.form.as_ul(), action="this action unknown" )
        return retval

    def get_css_class(self):
        return "jswidgets-imageformset"
