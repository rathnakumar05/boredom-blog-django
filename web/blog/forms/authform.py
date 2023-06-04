from django import forms
from django.core.validators import EmailValidator, MaxLengthValidator, MinLengthValidator, RegexValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import UserCreationForm

from ..models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class" : "form-control",
        "placeholder" : "Email"
    }), validators=[ EmailValidator, MaxLengthValidator(limit_value=150), MinLengthValidator(limit_value=2) ])
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class" : "form-control",
        "placeholder" : "Username"
    }), validators=[MinLengthValidator(limit_value=3), MaxLengthValidator(limit_value=150), RegexValidator(r'^[a-zA-Z0-9_]+$', 'Only alphanumeric and underscore characters are allowed.')])
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class" : "form-control",
        "placeholder" : "Password"
    }), validators=[ MaxLengthValidator(limit_value=50), MinLengthValidator(limit_value=2) ])
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class" : "form-control",
        "placeholder" : "Confirm Password"
    }), validators=[ MaxLengthValidator(limit_value=50), MinLengthValidator(limit_value=2) ])

    class Meta:
        model = User
        fields = [ 'email', 'username', 'password1', 'password2' ]

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class" : "form-control",
        "placeholder" : "Email"
    }), validators=[ EmailValidator, MaxLengthValidator(limit_value=150), MinLengthValidator(limit_value=2) ])
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class" : "form-control",
        "placeholder" : "Password"
    }), validators=[ MaxLengthValidator(limit_value=50), MinLengthValidator(limit_value=2) ])

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class" : "form-control",
        "placeholder" : "Email"
    }), validators=[ EmailValidator, MaxLengthValidator(limit_value=150), MinLengthValidator(limit_value=2) ])

class ForgotPasswordChangeForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class" : "form-control",
        "placeholder" : "New Password"
    }), validators=[ MaxLengthValidator(limit_value=50), MinLengthValidator(limit_value=2), validate_password ])
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class" : "form-control",
        "placeholder" : "Confirm Password"
    }), validators=[ MaxLengthValidator(limit_value=50), MinLengthValidator(limit_value=2) ])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Confirm password is not same")
        return password2