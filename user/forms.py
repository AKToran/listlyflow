from typing import Any
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from . models import ContactUs

class CreateAccountForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address already exists.')
        return email
    
    def save(self, commit=True ):
        user = super().save(commit=False)
        if commit == True:
            user.is_active = False
            user.save()
        return user


class ContactUsForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(required=True)
    description = forms.CharField(widget=forms.TextInput(), required=True)
    class Meta:
        model = ContactUs
        fields = "__all__"

