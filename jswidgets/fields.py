from django import forms
from .widgets import MultiModelSelect, SingleModelSelect, Formset
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


class FormsetField(forms.Field):
    _is_jswidgets_field = True

    def __init__(self, form_class, **kwargs):
        self.field_name = None
        self.form_data = None
        self.form_class = form_class
        field_kwargs = {}
        field_kwargs['format'] = kwargs.pop('format', 'ul')
        self.widget = Formset(form_class, **field_kwargs)
        super(FormsetField, self).__init__("some label", )

    def prepare_to_be_cleaned(self, field_name, form_data):
        self.field_name = field_name
        self.form_data = {}
        for key, val in form_data.items():
            if key.startswith('jswidgets-%s' % field_name):
                shortkey = '-'.join(key.split('-')[2:])
                self.form_data[shortkey] = val

    def clean(self, value):
        import ipdb; ipdb.set_trace()
        return "formset"
