from django import forms
from django.contrib.auth.models import User
from .models import User_profile_info

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model=User
        fields=('username','email','password')


class User_profile_form(forms.ModelForm):
    class Meta():
        model=User_profile_info
        fields=('portfolio_site','profile_pic')  