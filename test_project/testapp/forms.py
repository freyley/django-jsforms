import jsforms
from django import forms
from .models import Author, Publisher, Book, Factory, BookFormat, Animal, Farm


class AuthorForm(forms.ModelForm):
    publisher = jsforms.SingleModelField(model=Publisher)
    books = jsforms.MultiModelField(
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
    book_formats = jsforms.FormsetField(
            BookFormatForm, # allow passing in model instead of modelform
            format="ul",
            # extra=0,
            # save_to="book_formats",
            # delete_if_removed = False
            # remove_callback -> a method on the form
            )
    '''
    book_formats = forms.ModelMultipleChoiceField(
            queryset=BookFormat.objects.all())
    '''


    class Meta:
        model = Factory
        exclude = "book_formats"




class AnimalForm(jsforms.ModelForm):
    image = jsforms.ThumbnailImageField(temporary_thumbnail="http://dummyimage.com/100x100")
    class Meta:
        model = Animal


class FarmForm(jsforms.ModelForm):
    image = jsforms.ThumbnailImageField()
    animals = jsforms.FormsetField(AnimalForm)

    class Meta:
        model = Farm
