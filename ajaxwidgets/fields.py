from django import forms
from .widgets import MultiModelSelect


class MultiModelField(forms.Field):

    def __init__(self, *args, **kwargs):
        if not 'model' in kwargs:
            raise Exception("MultiModelField requires a model to be instantiated")
        model = kwargs.pop('model')
        if not 'widget' in kwargs:
            kwargs['widget'] = MultiModelSelect(model)
        self.model = model
        super(MultiModelField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        # this is where we turn the string into a list of ids
        try:
            ids = [ int(v.strip()) for v in value.split(',')]
        except ValueError:
            raise forms.ValidationError("%s not a valid intlist" % value)

    def clean(self, value):
        ids = self.to_python(value)
        model_objects = []
        for id in ids:
            try:
                model_objects.append(self.model.objects.get(pk=id))
            except self.model.objects.DoesNotExist:
                raise forms.ValidationError("id %d not found" % id)
        return model_objects



