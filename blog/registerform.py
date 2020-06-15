from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


    def clean_email(self, *args, **kwargs):
        instance = self.instance
        print(instance)
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email__iexact=email)
        if instance is not None:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise forms.ValidationError("this email is already been used")
        return email

    def clean_username(self, *args, **kwargs):
        instance = self.instance
        print(instance)
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username__iexact=username)
        if instance is not None:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise forms.ValidationError("this username is already been used")
        return username
