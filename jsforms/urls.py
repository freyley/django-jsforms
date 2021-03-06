from django.conf import settings
from django.db.models import get_model
from django.conf.urls.defaults import patterns, url
from .views import search, image_upload
urllist = []

try:
    for model_name, search_field in settings.JSFORMS_MODELS:
        model = get_model(*model_name.split('.'))
        urllist.append(url(
            r'%s/%s/$' % (model._meta.app_label, model.__name__),
            search, 
            { 
                'search_field' : search_field, 
                'model' : model,
            },
            name="aw_search_%s_%s" % ( model._meta.app_label, model.__name__)))
except AttributeError: pass
try:
    if settings.JSFORMS_IMAGEUPLOAD_FEATURE:
        urllist.append(url(r'image_upload/$',
                image_upload,
                name="jsforms_image_upload"))
except AttributeError: pass

urlpatterns = patterns('', *urllist)
