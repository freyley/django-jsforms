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
        self.save_to = kwargs.pop('save_to', self.field_name)
        widget_kwargs = {}
        widget_kwargs['format'] = kwargs.pop('format', 'ul')
        widget_kwargs['extra'] = kwargs.pop('extra', 2)
        self.widget = Formset(form_class, **widget_kwargs)
        super(FormsetField, self).__init__("some label", )

    def prepare_to_be_cleaned(self, field_name, form_data):
        self.field_name = field_name
        self.form_data = {}
        for key, val in form_data.items():
            if key.startswith('jswidgets-%s' % field_name):
                self.form_data[key] = val

    def clean(self, value):
        # TODO: turn the data in self.form_data into a formset
        fs_class = forms.formsets.formset_factory(self.form_class)
        fs = fs_class(self.form_data, prefix='jswidgets-%s' % self.field_name)
        if fs.is_valid():
            return fs.forms
        else:
            raise forms.ValidationError(fs.errors)

    def prepare_value(self, value):
        import ipdb; ipdb.set_trace()
        '''
        if hasattr(value, '__iter__'):
            return [super(ModelMultipleChoiceField, self).prepare_value(v) for v in value]
        return super(ModelMultipleChoiceField, self).prepare_value(value)
        '''

