AJAX widgets for Django

REQUIREMENTS:
Django 1.3



INSTALLATION INSTRUCTIONS

---- add this to urls.py ----

    # django-jsforms
    (r'^jsforms-api/', include('jsforms.urls')),



---- in settings.py... ----

# add the following
JSFORMS_MODELS = (
    ("some_app.SomeModel", "some_field"),
    ("pages.Page", "title"),
)

# make sure the following are in INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'jsforms',
]

# notes on django-staticfiles
# NOTE - when you use staticfiles you can't have files in your static root.
# NOTE - don't server static files in your urls.py



---- install django-staticfiles ----
make sure django.contrib.staticfiles

