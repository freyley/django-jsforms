# Create your views here.

from lib.decorators import template
from .forms import AuthorForm, FactoryForm
from .models import Author, Factory

@template("base.html")
def demo(request):
    return {}

@template("author.html")
def author(request):
    if request.method == "POST":
        author_form = AuthorForm(request.POST)
        if author_form.is_valid():
            author_form.save()
    else:
        author_form = AuthorForm()
    return dict(
        author_form = author_form,
        authors = Author.objects.all()
        )

@template("factory.html")
def factory(request):
    if request.method == "POST":
        factory_form = FactoryForm(request.POST)
        if factory_form.is_valid():
            factory_form.save()
    else:
        factory_form = FactoryForm()
    return dict(
        factory_form = factory_form,
        factories = Factory.objects.all()
        )

