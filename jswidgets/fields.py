from django import forms
from .widgets import MultiModelSelect, SingleModelSelect
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
