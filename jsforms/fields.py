from django import forms
from .widgets import MultiModelSelect, SingleModelSelect, Formset, \
        ThumbnailImage
from .tools import idstring_to_list, idlist_to_models
from .models import TemporaryUploadedImage
from django.core.files.storage import default_storage
#from .modelformset import BaseModelFormSet

import pprint
pp = pprint.PrettyPrinter(indent=2)

class SingleModelField(forms.ModelChoiceField):
    def __init__(self, *args, **kwargs):
        if not 'model' in kwargs:
            raise Exception("SingleModelField requires a model")
        self.model = kwargs.pop("model")
        if not "widget" in kwargs:
            kwargs["widget"] = SingleModelSelect(self.model)
        kwargs["queryset"] = self.model.objects.all()
        super(SingleModelField, self).__init__(*args, **kwargs)


class MultiModelField(forms.ModelMultipleChoiceField):
    _is_jsforms_field = True

    def __init__(self, *args, **kwargs):
        if not 'model' in kwargs:
            raise Exception("MultiModelField requires a model to be instantiated")
        model = kwargs.pop('model')
        widget_kwargs = {}
        for my_kwarg in ("dropdown_item_template", "list_item_template"):
            if my_kwarg in kwargs:
                widget_kwargs[my_kwarg] = kwargs.pop(my_kwarg)
        if not 'widget' in kwargs:
            kwargs['widget'] = MultiModelSelect(model, **widget_kwargs)
        self.model = model
        super(MultiModelField, self).__init__(*args, queryset=model.objects.all(),  **kwargs)

    def to_python(self, value):
        return idstring_to_list(value)

    def clean(self, value):
        ids = self.to_python(value)
        return idlist_to_models(ids, self.model)


class FormsetField(forms.Field):
    _is_jsforms_field = True
    _jsforms_saves_as_forms = True

    def __init__(self, form_class, **kwargs):
        self.field_name = None
        self.form_data = None
        self.form_class = form_class
        self.save_to = kwargs.pop('save_to', None)
        widget_kwargs = {}
        widget_kwargs['extra'] = kwargs.pop('extra', 0)
        widget_kwargs['format'] = kwargs.pop('format', 'ul')
        widget_kwargs['template'] = kwargs.pop('template', None)
        self.widget = Formset(form_class, **widget_kwargs)
        super(FormsetField, self).__init__("some label", )

    def prepare_to_be_cleaned(self, field_name, form_data):
        print "prepare_to_be_cleaned %s" % field_name
        self.field_name = field_name
        if not self.save_to:
            self.save_to = self.field_name
        self.form_data = {}
        for key, val in form_data.items():
            if key.startswith('jsforms-%s' % field_name):
                self.form_data[key] = val

    def clean(self, value):
        print "clean %s" % value
        pp.pprint(self.form_data)

        FSClass = forms.formsets.formset_factory(
                self.form_class, 
                forms.models.BaseModelFormSet,
                can_delete=True)
        FSClass.model = self.form_class._meta.model
        fs = FSClass(self.form_data, prefix='jsforms-%s' % self.field_name)
        if fs.is_valid():
            return fs.forms
        else:
            raise forms.ValidationError(fs.errors)

class ThumbnailImageField(forms.Field):
    _is_jsforms_field = True

    def __init__(self, *args, **kwargs):
        widget_kwargs = {}
        for key in 'upload_text', 'change_text', 'temporary_thumbnail':
            if key in kwargs:
                widget_kwargs[key] = kwargs.pop(key)
        self.widget = ThumbnailImage(**widget_kwargs)
        super(ThumbnailImageField, self).__init__(*args, **kwargs)

    def prepare_to_be_cleaned(self, field_name, form_data):
        self.field_name = field_name

    def clean(self, value, initial=None):
        try:
            tmp = TemporaryUploadedImage.objects.get(id=value)
            self.temporary_instance = tmp
            return tmp.timage.file
        except ValueError:
            try:
                opened_file = default_storage.open(value)
                return opened_file

            except IOError, ioe:
                raise forms.ValidationError("Image failed %s" % str(ioe))

    def clear(self, *args, **kwargs):
        pass
