from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Example:
    # (r'^test_project/', include('test_project.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^jswidgets-api/', include('jswidgets.urls')),
    url(r'^$', 'testapp.views.demo', name="demo"),
    url(r'^authors$', 'testapp.views.author', name="authors"),
    url(r'^authors/(?P<author_id>\d+)$', 'testapp.views.edit_author', name="edit_author"),
    url(r'^factories$', 'testapp.views.factory', name="factories"),
    url(r'^factories/(?P<factory_id>\d+)$', 'testapp.views.edit_factory', name="edit_factory"),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        # Static files (FOR DEVELOPMENT ONLY!)
         (r'^' + settings.MEDIA_URL.strip('/')+'/(?P<path>.*)$', 
                'django.views.static.serve',
                 {'document_root': settings.MEDIA_ROOT}),
         (r'^' + settings.STATIC_URL.strip('/')+'/(?P<path>.*)$', 
                'django.views.static.serve',
                 {'document_root': settings.STATIC_ROOT}),

    )
