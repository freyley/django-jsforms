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
        # this is where we turn the ids into model objects
        import ipdb; ipdb.set_trace()
