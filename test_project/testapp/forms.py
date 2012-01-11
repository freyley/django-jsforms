from jswidgets import fields as jsfields
from jswidgets import forms as jsforms
from django import forms
from .models import Author, Publisher, Book, Factory, BookFormat


class AuthorForm(forms.ModelForm):
    publisher = jsfields.SingleModelField(model=Publisher)
    books = jsfields.MultiModelField(
            model=Book,
            required=False,
            # list_item_template="list_item_override.js.tmpl",
            # dropdown_item_template="dropdown_item_override.js.tmpl",
            )

    class Meta:
        model = Author


class BookFormatForm(forms.ModelForm):

    class Meta:
        model = BookFormat


class FactoryForm(jsforms.ModelForm):
    book_formatssss = jsfields.FormsetField(
            BookFormatForm,
            format="ul",
            extra=1,
            save_to="book_formats",
            )

    class Meta:
        model = Factory
        exclude = "book_formats"

