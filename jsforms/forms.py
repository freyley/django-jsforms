from django import forms
from django.forms.forms import BoundField as django_BoundField
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from . import models

class BoundField(django_BoundField):
    def __init__(self, form, field, name):
        super(BoundField, self).__init__(form, field, name)
        self.field._form = form
        self.field.widget._field = self.field

class ModelForm(forms.ModelForm):
    bound_field_class = BoundField
    
    def __iter__(self):
        for name, field in self.fields.items():
            yield self.bound_field_class(self, field, name)

    def __getitem__(self, name):
        "Returns a BoundField with the given name."
        try:
            field = self.fields[name]
        except KeyError:
            raise KeyError('Key %r not found in Form' % name)
        return self.bound_field_class(self, field, name)

    def _html_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        "Helper function for outputting HTML. Used by as_table(), as_ul(), as_p()."
        top_errors = self.non_field_errors() # Errors that should be displayed above all fields.
        output, hidden_fields = [], []

        for name, field in self.fields.items():
            html_class_attr = ''
            bf = self.bound_field_class(self, field, name)
            bf_errors = self.error_class([conditional_escape(error) for error in bf.errors]) # Escape and cache in local variable.
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend([u'(Hidden field %s) %s' % (name, force_unicode(e)) for e in bf_errors])
                hidden_fields.append(unicode(bf))
            else:
                # Create a 'class="..."' atribute if the row should have any
                # CSS classes applied.
                css_classes = bf.css_classes()
                if css_classes:
                    html_class_attr = ' class="%s"' % css_classes

                if errors_on_separate_row and bf_errors:
                    output.append(error_row % force_unicode(bf_errors))

                if bf.label:
                    label = conditional_escape(force_unicode(bf.label))
                    # Only add the suffix if the label does not end in
                    # punctuation.
                    if self.label_suffix:
                        if label[-1] not in ':?.!':
                            label += self.label_suffix
                    label = bf.label_tag(label) or ''
                else:
                    label = ''

                if field.help_text:
                    help_text = help_text_html % force_unicode(field.help_text)
                else:
                    help_text = u''

                output.append(normal_row % {
                    'errors': force_unicode(bf_errors),
                    'label': force_unicode(label),
                    'field': unicode(bf),
                    'help_text': help_text,
                    'html_class_attr': html_class_attr
                })

        if top_errors:
            output.insert(0, error_row % force_unicode(top_errors))

        if top_errors:
            output.insert(0, error_row % force_unicode(top_errors))

        if hidden_fields: # Insert any hidden fields in the last row.
            str_hidden = u''.join(hidden_fields)
            if output:
                last_row = output[-1]
                # Chop off the trailing row_ender (e.g. '</td></tr>') and
                # insert the hidden fields.
                if not last_row.endswith(row_ender):
                    # This can happen in the as_p() case (and possibly others
                    # that users write): if there are only top errors, we may
                    # not be able to conscript the last row for our purposes,
                    # so insert a new, empty row.
                    last_row = (normal_row % {'errors': '', 'label': '',
                                              'field': '', 'help_text':'',
                                              'html_class_attr': html_class_attr})
                    output.append(last_row)
                output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
            else:
                # If there aren't any rows in the output, just append the
                # hidden fields.
                output.append(str_hidden)
        return mark_safe(u'\n'.join(output))


    def full_clean(self, *args, **kwargs):

        for name, field in self.fields.items():
            try:
                field._is_jsforms_field
            except AttributeError:
                continue
            field.prepare_to_be_cleaned(name, self.data)

        super(ModelForm, self).full_clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        cleaned_data_minus_formsavers = {}
        formsavers_formlists = {}
        for key, val in self.cleaned_data.items():
            try:
                self.fields[key]._jsforms_saves_as_forms
                formsavers_formlists[key] = val
            except AttributeError:
                cleaned_data_minus_formsavers[key] = val
        self.cleaned_data = cleaned_data_minus_formsavers
        instance = super(ModelForm, self).save(*args, **kwargs)

        def save_forms():
            for field_name, formlist in formsavers_formlists.items():

                try: 
                    model_field = self.fields[field_name].save_to
                except AttributeError:
                    model_field = field_name
                obj_field = getattr(instance, model_field)
                obj_field.clear()
                for form in formlist:
                    if hasattr(form, 'is_empty'):
                        if callable(form.is_empty):
                            if form.is_empty():
                                continue
                        else:
                            if form.is_empty:
                                continue
                    else:
                        if not form.cleaned_data:
                            continue
                    if form.cleaned_data['DELETE']:
                        # TODO: if we have delete-removed, delete this object
                        pass
                    else:
                        obj_field.add(form.save())

        commit = kwargs.get('commit', True)
        if commit:
            save_forms()
            print "commit was true"
        else:
            _old_save_m2m = self.save_m2m
            def save_m2m_2():
                _old_save_m2m()
                save_forms()
            self.save_m2m = save_m2m_2
        return instance

        
class SearchForm(forms.Form):
    term = forms.CharField()


class TemporaryUploadedImageForm(forms.ModelForm):
    class Meta:
        model = models.TemporaryUploadedImage
