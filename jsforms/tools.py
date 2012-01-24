from django import forms
from django.conf import settings

def idstring_to_list(value):
    # this is where we turn the string into a list of ids
    if len(value) == 0:
        return []
    try:
        return [ int(v.strip()) for v in value.split(',')]
    except ValueError:
        raise forms.ValidationError("%s not a valid intlist" % value)
    except AttributeError:
        return []

def idlist_to_models(ids, model):
    model_objects = []
    for id in ids:
        try:
            model_objects.append(model.objects.get(pk=id))
        except model.DoesNotExist:
            raise forms.ValidationError("id %d not found" % id)
    return model_objects

def get_display_field(model):
    searchstring = "%s.%s" % ( model._meta.app_label, model.__name__)
    try:
        for mod, field in settings.JSFORMS_MODELS:
            if mod == searchstring:
                return field
    except AttributeError: pass
