from django import forms
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from dyno.models import Card_Info, Well_Profile, Dysfunction_Profile
from dyno.utils.choices import well_choice_gen
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
        fields = ('associated_well_profile', 'title', 'img_file', 'card_description', 'actual_total_prod')
        widgets = {
        'title': forms.TextInput(attrs={'placeholder': 'Suggested format = Well Name -- Card Number'}),
        'card_description': forms.TextInput(attrs={'placeholder': 'Describe what you suspect may be happening here!'}),
        }

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
            'well_name': forms.TextInput(attrs={'placeholder': 'Please Enter Well Name', 'required': True}),
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

    well_name = forms.ChoiceField(
                                label = 'Well Name:',
                                choices = well_choice_gen(),
                                widget = forms.Select()
                                )

    def __init__(self, *args, **kwargs):
        super(DirectoryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-group'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
                Div(
                    HTML('''<br/>
                            <label for="input_dir">Input Directory:</label>
                                <input name = input_dir type="text" id="input_dir" class="form-control" aria-describedby="inputHelpBlock">
                                <small id="inputHelpBlock" class="form-text text-muted">
                                  Please be sure to specify the folder structure as "/path/to/dir/predict/insert_well_name/all_images.jpg"
                                </small>
                                <br/>'''),
                    Field('well_name', css_class = "form-control", describedby = "wellHelpBlock"),
                    HTML('''<small id = "wellHelpBlock" class="form-text text-danger">
                                            *If your well is not in this dropdown list, please create well to assign cards to before analyzing and predicting.
                                            </small>
                                            </br>'''),
                        Div(
                                Div(Submit('submit', 'Analyze Directory', css_class = "btn btn-outline-success"),
                                    HTML('''<a href="{% url 'dyno:well_information' %}" class="btn btn-outline-secondary" >Create Well</a>'''),
                                    css_class ="col-sm-12 text-left"),
                            css_class = 'row'),
                    css_class = 'container-fluid',)
                    )

class CrispyDysfunctionModelForm(forms.ModelForm):
    class Meta:
        model = Dysfunction_Profile
        fields = '__all__'
        widgets = {
            'dys_name': forms.TextInput(attrs={'placeholder': 'Please enter Dysfunction Name', 'required': True}),
            'dys_description': forms.TextInput(attrs={'placeholder': 'Please describe the cause of this dysfunction', 'required': True}),
            'dys_action': forms.TextInput(attrs={'placeholder': 'Please state actions to remediate the dysfunction', 'required': True})
        }

    def __init__(self, *args, **kwargs):
        super(CrispyDysfunctionModelForm, self).__init__(*args, **kwargs)
        self.fields['dys_name'].label = "Dysfunction Name:"
        self.fields['dys_description'].label = "Cause of Dysfunction:"
        self.fields['dys_action'].label = "Remediation Steps:"
        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        # You can dynamically adjust your layout
        self.helper.layout.append(Submit('Submit', 'Submit'))
