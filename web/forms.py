from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name","email", "mob", "message"]

        widgets = {
            "name":forms.widgets.TextInput(attrs={"class": "form-control","placeholder":"Full Name"}),
            "email":forms.widgets.EmailInput(attrs={"class": "form-control","placeholder":"Email"}),
            "mob":forms.widgets.NumberInput(attrs={"class": "form-control","placeholder":"Mobile"}),
            "message" : forms.widgets.TextInput(attrs={"class": "form-control","placeholder":"Password"})
        }
