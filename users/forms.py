from django import forms
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth import authenticate

from .models import User, Company, Customer


class DateInput(forms.DateInput):
    input_type = 'date'

# Customer Registration Form class
class CustomerSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    birth = forms.DateField(widget=DateInput, required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")


        if password and password2 and password != password2:
            self.add_error("password_confirmation", "passwords don't match")

class CustomerLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget = forms.PasswordInput)


# Company Registration Form
class CompanySignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    field = forms.ChoiceField(choices=Company._meta.get_field("field").choices)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]

    def clean(self):
       cleaned_data = super().clean()
       password = cleaned_data.get("password")
       password2 = cleaned_data.get("password2")
       
       if password and password2 and password != password2:
        self.add_error('password_confirm', "Passwords don't match")

class LoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
    
    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(email = email, password=password)
        if not user:
            raise forms.ValidationError("Invalid email or passward")
        return self.cleaned_data
