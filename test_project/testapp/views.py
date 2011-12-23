# Create your views here.

from lib.decorators import template
from .forms import BarForm
from .models import Bar

@template("foo.html")
def foo(request):
    if request.method == "POST":
        form = BarForm(request.POST)
        if form.is_valid():
            form.save()
    else:

        form = BarForm()
    return dict(
        form = form,
        bars = Bar.objects.all()
        )
