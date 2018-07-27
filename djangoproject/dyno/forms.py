from django import forms
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from dyno.models import Card_Info, Well_Profile, Dysfunction_Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class ImageForm(forms.ModelForm):
    class Meta:
        model = Card_Info
        fields = ('associated_well_profile', 'title', 'img_file')

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        # You can dynamically adjust your layout
        self.helper.layout.append(Submit('Submit', 'Submit'))




class CrispyModelForm(forms.ModelForm):
    class Meta:
        model = Well_Profile
        fields = '__all__'
        widgets = {
            'well_name': forms.TextInput(attrs={'placeholder': 'Please Enter Well Name','required': True}),
            'pumping_unit': forms.TextInput(attrs={'placeholder': 'Please Enter Pumping Unit', 'required': True})
        }

    def __init__(self, *args, **kwargs):
        super(CrispyModelForm, self).__init__(*args, **kwargs)
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        # You can dynamically adjust your layout
        self.helper.layout.append(Submit('Submit', 'Submit'))


class DirectoryForm(forms.Form):
    input_dir = forms.CharField(
                        label = 'Directory:',
                        widget=forms.TextInput(attrs={'placeholder':'Please enter directory path'})
                        )
    well_name = forms.CharField(
                        label = 'Well Name:',
                        widget=forms.TextInput(attrs={'placeholder':'Please enter well name'})
                        )

    def __init__(self, *args, **kwargs):
        super(DirectoryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-group'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
                Div(
                    Field('input_dir', css_class="form-group"),
                    Field('well_name', css_class = "form-group"),
                    Div(

                        Div(Submit('submit', 'Analyze Directory', css_class = "btn btn-success"), css_class = 'col-sm'),
                        css_class = 'row'),

                    css_class = 'container-fluid',
            ))
