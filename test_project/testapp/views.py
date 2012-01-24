# Create your views here.

from lib.decorators import template
from .forms import AuthorForm, FactoryForm, FarmForm, AnimalForm
from .models import Author, Factory, Farm, Animal


@template("base.html")
def demo(request):
    return {}




@template("authors.html")
def authors(request):
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


@template("edit_author.html")
def edit_author(request, author_id):
    pass




@template("factories.html")
def factories(request):
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

@template("edit_factory.html")
def edit_factory(request, factory_id):
    factory = Factory.objects.get(id=factory_id)
    if request.method == "POST":
        factory_form = FactoryForm(request.POST, instance=factory)
        if factory_form.is_valid():
            factory_form.save()
    else:
        factory_form = FactoryForm(instance=factory)
    return dict(
        factory_form = factory_form,
        factories = Factory.objects.all()
        )




@template("farms.html")
def farms(request):
    if request.method == "POST":
        farm_form = FarmForm(request.POST)
        if farm_form.is_valid():
            farm_form.save()
    else:
        farm_form = FarmForm()
    return dict(
        farm_form = farm_form,
        farms = Farm.objects.all(),
        )


@template("edit_farm.html")
def edit_farm(request, farm_id):
    farm = Farm.objects.get(id=farm_id)
    farm_form = FarmForm()
    return dict(
        farm_form = farm_form,
        farm = farm,
        )
