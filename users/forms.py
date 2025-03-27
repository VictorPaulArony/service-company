from django import forms
from django.contrib.auth.forms import  AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from .models import User, Company, Customer


class DateInput(forms.DateInput):
    input_type = 'date'


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            value + " is already taken.")


# Customer Registration Form class
class CustomerSignUpForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        widget=forms.TextInput(attrs={'placeholder': "Enter Username",'style': 'width: 100%;'})
    )

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': "Enter Password",'style': 'width: 100%;'}),
        help_text= [
            "Your paasword can't be too similar to your other personal information.",
            "Your paasword must contain at least 8 characters.",
            "Your paasword can't be a commonly used password.",
            "Your paasword can't be entirely numeric."
        ])
    
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': "Re-Entre same Password",'style': 'width: 100%;'}),
        help_text= "Entre the same password as before, for verification.")
    
    email = forms.EmailField(
        required=True,
        validators=[validate_email], 
        widget=forms.EmailInput(attrs={'placeholder': "Enter Email",'style': 'width: 100%;'})
    )

    date_of_birth = forms.DateField(
        required=True,
        widget=DateInput(attrs={'placeholder': 'MM/DD/YYYY','style': 'width: 100%;'}) 
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2",  "email", "date_of_birth"]

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
class CompanySignUpForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': "Enter Username",'style': 'width: 100%;'}),
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': "Enter password",'style': 'width: 100%;'}),
            help_text=[
            "Your paasword can't be too similar to your other personal information.\n",
            "Your paasword must contain at least 8 characters.\n",
            "Your paasword can't be a commonly used password.\n",
            "Your paasword can't be entirely numeric."
        ])
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': "Re-Entre same Password",'style': 'width: 100%;'}),
        help_text= "Entre the same password as before, for verification."
    )

    email = forms.EmailField(
        required=True,
        validators=[validate_email], 
        widget=forms.EmailInput(attrs={'placeholder': "Enter Email",'style': 'width: 100%;'})
    )
    field_of_work = forms.ChoiceField(
        choices=[('', '--- Select ---')] + list(Company.FieldOfWork.choices),
        required=True,
        widget=forms.Select(attrs={'style': 'width: 100%;'})
    )

    class Meta:
        model = User
        fields = ["username", "password", "password2", "email", "field_of_work",]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_company = True
        if commit:
            user.save()
            Company.objects.create(user=user, field=self.cleaned_data['field_of_work'])
        return user

class UserLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Email',
               'style': 'width: 100%;'}))
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password',
                                          'style': 'width: 100%;'}))

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['autocomplete'] = 'off'