from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ActivityForm(forms.Form):
    act_name = forms.CharField(max_length=64)
    location = forms.CharField(max_length=64)
    time = forms.DateTimeField()
    description = forms.CharField(max_length=5000)
    loc_lat = forms.FloatField()
    loc_long = forms.FloatField()


class PersonForm(forms.Form):
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(required=False, help_text='Optional.')
    last_name = forms.CharField(required=True, help_text='Required.')
    email = forms.EmailField(help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


