# Create your views here.

from lib.decorators import template
from .forms import AuthorForm, FactoryForm
from .models import Author

@template("demo.html")
def demo(request):
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
