from django import forms
from django.contrib.auth.models import User


class SignupForm(forms.Form):
    email = forms.EmailField()
    organization_name = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean(self):
        data = super().clean()
        if data.get("password") != data.get("confirm_password"):
            self.add_error("confirm_password", "Passwords do not match.")
        return data