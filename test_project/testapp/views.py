# Create your views here.

from lib.decorators import template

@template("foo.html")
def foo(request):
    return dict()
