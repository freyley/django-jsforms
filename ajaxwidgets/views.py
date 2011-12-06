from django.http import HttpResponse
from django import forms

class SearchForm(forms.Form):
    q = forms.CharField()

from lib.decorators import jsonapi

@jsonapi
def search(request, **kwargs):
    model = kwargs["model"]
    search_field = kwargs["search_field"]
    form = SearchForm(request.GET)
    if form.is_valid():
        objs = model.objects.filter(**{search_field+'__icontains':form.cleaned_data['q']})
    else:
        objs = model.objects.all()[:50]

    vals = objs.values(search_field, 'id')
    return list(vals)
