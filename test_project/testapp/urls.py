from django.conf.urls.defaults import *
urlpatterns = patterns(
    'testapp.views',
    url(r'^foo', 'foo', name="foo"),

)

