from django import forms
from .widgets import MultiModelSelect, SingleModelSelect

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
        # this is where we turn the string into a list of ids
        try:
            return [ int(v.strip()) for v in value.split(',')]
        except ValueError:
            raise forms.ValidationError("%s not a valid intlist" % value)

    def clean(self, value):
        ids = self.to_python(value)
        model_objects = []
        for id in ids:
            try:
                model_objects.append(self.model.objects.get(pk=id))
            except self.model.DoesNotExist:
                raise forms.ValidationError("id %d not found" % id)
        return model_objects
