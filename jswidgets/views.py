from django import forms
from . import models

class SearchForm(forms.Form):
    term = forms.CharField()

class TemporaryUploadedImageForm(forms.ModelForm):
    class Meta:
        model = models.TemporaryUploadedImage

from .decorators import jsonapi, textarea_api

@jsonapi
def search(request, **kwargs):
    model = kwargs["model"]
    search_field = kwargs["search_field"]

    form = SearchForm(request.GET)

    if form.is_valid():
        ids = request.GET.getlist("exclude[]")
        objs = model.objects\
                .filter(**{search_field+'__icontains':form.cleaned_data['term']})\
                .exclude(id__in=ids)
    else:
        objs = model.objects.all()[:50]

    field_data = objs.values_list(search_field, 'id')
    vals = [{'label' : fd[0], 'id' : fd[1]} for fd in field_data]
    return vals


@textarea_api
def image_upload(request):
    form = TemporaryUploadedImageForm(request.POST, request.FILES)
    if form.is_valid():
        tf = form.save()
        return dict( id = tf.id, success = True,
            thumbnail_url = "/asdf/foo.png")
    return dict( success = False, errors = form.errors)

