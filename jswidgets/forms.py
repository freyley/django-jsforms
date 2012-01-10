from django import forms



# AWESOME SHIT GOES HERE!!!!!

class ModelForm(forms.ModelForm):

    def full_clean(self, *args, **kwargs):

        for name, field in self.fields.items():
            try:
                field._is_jswidgets_field
            except AttributeError: 
                continue
            field.prepare_to_be_cleaned(name, self.data)

        super(ModelForm, self).full_clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        import ipdb; ipdb.set_trace()
        super(ModelForm, self).save(*args, **kwargs)

