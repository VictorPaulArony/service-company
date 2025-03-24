from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, authenticate
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import User, Company, Customer


class DateInput(forms.DateInput):
    input_type = 'date'


def validate_email(value):
    # In case the email already exists in an email input in a registration form, this function is fired
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            value + " is already taken.")

# Customer Registration Form
class CustomerSignUpForm(UserCreationForm):
    birth = forms.DateField(widget=DateInput, required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        Customer.objects.create(user=user, birth=self.cleaned_data.get("birth"))
        return user

class CustomerLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget = forms.PasswordInput)


# Company Registration Form
class CompanySignUpForm(UserCreationForm):
    field = forms.ChoiceField(choices=Company._meta.get_field("field").choices)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_company = True
        user.save()
        Company.objects.create(user=user, field=self.cleaned_data["field"])
        return user

class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['autocomplete'] = 'off'
