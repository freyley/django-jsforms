from django import forms


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
        cleaned_data_minus_jswidgets = {}
        jswidgets_formlists = {}
        for key, val in self.cleaned_data.items():
            try:
                self.fields[key]._is_jswidgets_field
                jswidgets_formlists[key] = val
            except AttributeError:
                cleaned_data_minus_jswidgets[key] = val
        self.cleaned_data = cleaned_data_minus_jswidgets
        instance = super(ModelForm, self).save(*args, **kwargs)

        def save_forms():
            for field_name, formlist in jswidgets_formlists.items():
                if self.fields[field_name].save_to: 
                    model_field = self.fields[field_name].save_to
                else:
                    model_field = field_name
                obj_field = getattr(instance, model_field)
                obj_field.clear()
                for form in formlist:
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
