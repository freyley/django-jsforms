from jswidgets import fields as jsfields
from django import forms
from .models import Foo, Bar, Baz

class BarForm(forms.ModelForm):
    foo = jsfields.SingleModelField(model=Foo)
    bazes = jsfields.MultiModelField(model=Baz, required=False)

    class Meta:
        model = Bar
        
