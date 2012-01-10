from jswidgets import fields as jsfields
from django import forms
from .models import Author, Publisher, Book, Factory, BookFormat


class AuthorForm(forms.ModelForm):
    publisher = jsfields.SingleModelField(model=Publisher)
    books = jsfields.MultiModelField(model=Book, required=False)

    class Meta:
        model = Author


class FactoryForm(forms.ModelForm):

    class Meta:
        model = Factory
