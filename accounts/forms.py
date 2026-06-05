from django import forms
from django.contrib.auth.models import User

from organizations.models import Organization
from roles.models import Role


class UserProfileForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={"class": "form-control"}))
    organization = forms.ModelChoiceField(queryset=Organization.objects.all(), widget=forms.Select(attrs={"class": "form-select"}))
    role = forms.ModelChoiceField(queryset=Role.objects.all(), widget=forms.Select(attrs={"class": "form-select"}))
    is_active = forms.BooleanField(required=False, initial=True)

    def __init__(self, *args, organization=None, **kwargs):
        super().__init__(*args, **kwargs)
        if organization is not None:
            self.fields["organization"].queryset = Organization.objects.filter(id=organization.id)
            self.fields["role"].queryset = Role.objects.filter(organization=organization)

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username


class UserUpdateForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={"class": "form-control"}))
    role = forms.ModelChoiceField(queryset=Role.objects.all(), widget=forms.Select(attrs={"class": "form-select"}))
    is_active = forms.BooleanField(required=False)

    def __init__(self, *args, organization=None, **kwargs):
        super().__init__(*args, **kwargs)
        if organization is not None:
            self.fields["role"].queryset = Role.objects.filter(organization=organization)
