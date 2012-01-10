from jswidgets import fields as jsfields
from jswidgets import forms as jsforms
from django import forms
from .models import Author, Publisher, Book, Factory, BookFormat


class AuthorForm(forms.ModelForm):
    publisher = jsfields.SingleModelField(model=Publisher)
    books = jsfields.MultiModelField(model=Book, required=False)

    class Meta:
        model = Author


class BookFormatForm(forms.ModelForm):

    class Meta:
        model = BookFormat


class FactoryForm(jsforms.ModelForm):
    book_formats = jsfields.FormsetField(BookFormatForm, format="ul", save_to="book_formats")

    class Meta:
        model = Factory


