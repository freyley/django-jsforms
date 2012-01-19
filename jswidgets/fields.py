from django import forms
from .widgets import MultiModelSelect, SingleModelSelect, ModelFormset, \
        ImageFormset
from .tools import idstring_to_list, idlist_to_models


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


class ModelFormsetField(forms.Field):
    _is_jswidgets_field = True

    def __init__(self, form_class, **kwargs):
        self.field_name = None
        self.form_data = None
        self.form_class = form_class
        self.save_to = kwargs.pop('save_to', self.field_name)
        widget_kwargs = {}
        widget_kwargs['extra'] = kwargs.pop('extra', 0)
        widget_kwargs['format'] = kwargs.pop('format', 'ul')
        widget_kwargs['template'] = kwargs.pop('template', None)
        self.widget = ModelFormset(form_class, **widget_kwargs)
        super(ModelFormsetField, self).__init__("some label", )

    def prepare_to_be_cleaned(self, field_name, form_data):
        self.field_name = field_name
        self.form_data = {}
        for key, val in form_data.items():
            if key.startswith('jswidgets-%s' % field_name):
                self.form_data[key] = val

    def clean(self, value):
        mfs_class = forms.models.modelformset_factory(
                self.form_class._meta.model, can_delete=True)
        mfs = mfs_class(self.form_data, prefix='jswidgets-%s' % self.field_name)

        if mfs.is_valid():
            return mfs.forms
        else:
            raise forms.ValidationError(mfs.errors)

class ImageFormsetField(forms.Field):
    _is_jswidgets_field = True
    widget = ImageFormset

    def prepare_to_be_cleaned(self, field_name, form_data):
        pass



