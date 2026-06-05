from django import forms

from .models import Role


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
