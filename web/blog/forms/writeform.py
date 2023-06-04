from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator
from django.templatetags.static import static
from django.contrib.staticfiles import finders

from ..models.post import Post

def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.size
    megabyte_limit = 2.0
    if filesize > megabyte_limit*1024*1024:
        raise forms.ValidationError("Max file size is %sMB" % str(megabyte_limit))

class WriteForms(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
                "class" : "form-control bg-dark text-white ",
                "placeholder" : "Title"
            }), validators=[MaxLengthValidator(limit_value=250), MinLengthValidator(limit_value=1), RegexValidator(r'^[a-zA-Z0-9_\s]+$', 'Only alphanumeric, underscore and space characters are allowed.')])
    description = forms.CharField(widget=forms.Textarea(attrs={
                "class" : "form-control bg-dark text-white  ",
                "placeholder" : "Description",
                "rows" : 3
            }), validators=[MaxLengthValidator(limit_value=500), MinLengthValidator(limit_value=1), RegexValidator(r'^[A-Za-z0-9_+-.,\'\"\(\)\{\}\s]*$', 'Only alphanumeric, underscore, +, (), {},,,.,\'," and space characters are allowed.')])
    author = forms.CharField(widget=forms.TextInput(attrs={
                "class" : "form-control bg-dark text-white  ",
                "placeholder" : "Author name"
            }), validators=[MaxLengthValidator(limit_value=150), MinLengthValidator(limit_value=1), RegexValidator(r'^[a-zA-Z0-9_\s]+$', 'Only alphanumeric, underscore and space characters are allowed.')])
    tumbnail = forms.FileField(widget=forms.ClearableFileInput(attrs={
        "class" : "form-control bg-dark text-white  ",
        "placeholder" : "Upload Nail",
        "id" : "tumbnail"
    }), validators=[validate_image], required=False)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

        if self.instance:
            self.fields['title'].initial = self.instance.title
            self.fields['description'].initial = self.instance.description
            self.fields['author'].initial = self.instance.author