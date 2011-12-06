from django import forms
from django.core.urlresolvers import reverse
#from django.utils.safestring import mark_safe

class SingleModelSelect(forms.TextInput):
    """ 
    Use this to select a single instance of a model
    with too many to have a simple select field.
    Must be used on a field with a queryset variable
    """

    def __init__(self, model, *args, **kwargs):
        self.model = model
        super(SingleModelSelect, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        new_attrs = attrs.copy()
        css = new_attrs.get('class', '')
        if css:
            css += ' '
        css += 'ajax_widget_singleselect ajax_widget'
        new_attrs['class'] = css
        new_attrs['data-sourceurl'] = reverse(
            "aw_search_%s_%s" % (self.model._meta.app_label, 
                                 self.model.__name__)
            )

        return super(SingleModelSelect, self).render(name, value, new_attrs)
