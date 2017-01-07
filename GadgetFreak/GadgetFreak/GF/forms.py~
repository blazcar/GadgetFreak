from django import forms
from .models import Article, User

class LoginForm(forms.Form):
  username = forms.CharField(label='Uporabnisko ime', max_length=100)
  password = forms.CharField(label='Geslo', max_length=100, widget=forms.PasswordInput)

class UserForm(forms.Form):
  username = forms.CharField(label='Uporabnisko ime', max_length=100)
  password = forms.CharField(label='Geslo', max_length=100, widget=forms.PasswordInput)
 	#email = forms.EmailField(label='Email')



