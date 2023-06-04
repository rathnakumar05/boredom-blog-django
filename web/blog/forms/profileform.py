from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator
from django.forms import ModelForm
from ..models import Profile

def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.size
    megabyte_limit = 2.0
    if filesize > megabyte_limit*1024*1024:
        raise forms.ValidationError("Max file size is %sMB" % str(megabyte_limit))


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'about', 'profile_pic']

    first_name = forms.CharField(widget=forms.TextInput(attrs={
                "class" : "form-control bg-dark text-white ",
                "placeholder" : "First Name"
            }), validators=[MaxLengthValidator(limit_value=50), MinLengthValidator(limit_value=1), RegexValidator(r'^[a-zA-Z0-9_\s]+$', 'Only alphanumeric, underscore and space characters are allowed.')])

    last_name = forms.CharField(widget=forms.TextInput(attrs={
                "class" : "form-control bg-dark text-white ",
                "placeholder" : "Last Name"
            }), validators=[MaxLengthValidator(limit_value=50), MinLengthValidator(limit_value=1), RegexValidator(r'^[a-zA-Z0-9_\s]+$', 'Only alphanumeric, underscore and space characters are allowed.')])

    about = forms.CharField(widget=forms.Textarea(attrs={
                "class" : "form-control bg-dark text-white ",
                "placeholder" : "About",
                "rows" : 3
            }), validators=[MaxLengthValidator(limit_value=50), MinLengthValidator(limit_value=1), RegexValidator(r'^[a-zA-Z0-9_\s]+$', 'Only alphanumeric, underscore and space characters are allowed.')])

    profile_pic = forms.ImageField(required=True, widget=forms.ClearableFileInput(attrs={
                "class" : "form-control bg-dark text-white ",
                "accept" : "image/*",
                "multiple" : False
            }), validators=[validate_image])