from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import loader, Context
from django.utils import simplejson as sj
from django.utils.safestring import mark_safe

from .models import TemporaryUploadedImage
from .tools import idstring_to_list, idlist_to_models, get_display_field
from .utils import image_to_thumb_url
from .modelformset import BaseModelFormSet

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
        new_attrs['data-target_id'] = new_attrs['id']
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
        return "jsforms-singleselect"

class MultiModelSelect(SingleModelSelect):

    def __init__(self, model, *args, **kwargs):
        self.list_item_template = "jsforms/multimodelselect/list_item.js.tmpl"
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
            existing_data = "data-existing_data='%s'" % urllib.quote(sj.dumps(field_data))
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
        return "jsforms-multiselect"



class Formset(forms.TextInput):

    def __init__(self, form_class, *args, **kwargs):
        self.format = kwargs.pop('format', None)
        self.template = kwargs.pop('template', None)
        self.extra = kwargs.pop('extra', 0)
        if self.template:
            self.format = 'template'

        self.form_class = form_class
        super(Formset, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        field_name = self._field.save_to or name
        FSClass = forms.formsets.formset_factory(
                self.form_class,
                BaseModelFormSet,
                can_delete=True,
                extra=self.extra)
        FSClass.model = self.form_class._meta.model
        kwargset = { 'prefix' : 'jsforms-%s' % name }

        try:
            dataset = getattr(self._field._form.instance, field_name).all()
            kwargset['queryset'] = dataset
        except ValueError:
            kwargset['queryset'] = self.form_class._meta.model.objects.none()
        if self._field._form.is_bound and not self._field._form.is_valid():
            kwargset['initial'] = self._field.form_data
        kwargset['initial'] = [dict(height=123, width=345, max_pages=456)]
        fs = FSClass(**kwargset)

        script_open = '<script type="text/template" class="jsforms-formsetfield-template" data-name="%s">' % name
        add_button = '<a class="jsforms-formsetfield-addform-%s" href="#">add form</a>' % name

        if self.format == 'ul':
            open_ul = '<ul class="jsforms-formsetfield-form-%s">' % name
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
            return '%s<script class="jsforms-formsetfield" type="text/template">%s</script>' % (fs.as_p(), fs.empty_form.as_p())
        elif self.format == 'template':
            # TODO
            return "a template"



class ThumbnailImage(forms.TextInput):
    """
    Use this to upload an image and get a thumbnail back
    """
    def __init__(self, *args, **kwargs):
        self.upload_text = kwargs.pop('upload_text', "upload image")
        self.change_text = kwargs.pop("change_text", "change image")
        self.temporary_thumbnail = kwargs.pop("temporary_thumbnail",
                None)
        self.thumbnail_generator = kwargs.pop("thumbnail_generator", image_to_thumb_url)
        super(ThumbnailImage, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        # print "NAME: %s, VALUE: %s" % (name, value)

        new_attrs = attrs.copy()
        css_class = self.get_css_class()
        css = new_attrs.get('class', '')
        if css:
            css += ' '
        css += css_class
        new_attrs['class'] = css

        hidden_attrs = attrs.copy()
        hidden_attrs['type'] = 'hidden'
        hidden = super(ThumbnailImage, self).render(name, value, hidden_attrs)
        # TODO: also if there's a thumbnail for the value
        # not sure what value looks like yet
        image_tag = ""
        if self.temporary_thumbnail:
            image_tag = '<img src="%s" id="%s_image_tag">' % (self.temporary_thumbnail, new_attrs['id'])
        if value:
            try:
                id = int(value)
                tmp_img = TemporaryUploadedImage.objects.get(id=id)
                image_tag = '<img src="%s" id="%s_image_tag">' % (
                        self.thumbnail_generator(name=name, image=tmp_img.timage),
                        new_attrs['id'],
                        )
            except ValueError:
                image_tag = '<img src="%s" id="%s_image_tag">' % (
                        self.thumbnail_generator(name=name, image=value),
                        new_attrs['id'],
                        )

        html = '''
                %(hidden)s
                %(image_tag)s
               <button class="%(css_class)s"
               data-hidden_id="%(hidden_id)s"
               data-upload_url="%(action)s"
               data-upload_image_text="%(upload_text)s"
               data-change_image_text="%(change_text)s">upload image</button>
        ''' % dict(css_class=css_class, name=name, 
                    hidden = hidden,
                    hidden_id = new_attrs['id'],
                    image_tag=image_tag,
                    upload_text="upload image",
                    change_text="change image",
                    action=reverse("jsforms_image_upload"))
        return html

    def get_css_class(self):
        return "jsforms-thumbnailimage"
