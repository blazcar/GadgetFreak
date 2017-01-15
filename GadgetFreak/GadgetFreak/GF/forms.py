from django import forms
from .models import Article, User, Comment

class LoginForm(forms.Form):
  username = forms.CharField(label='Uporabnisko ime', max_length=100)
  password = forms.CharField(label='Geslo', max_length=100, widget=forms.PasswordInput)

class UserForm(forms.Form):
  username = forms.CharField(label='Uporabnisko ime', max_length=100)
  password = forms.CharField(label='Geslo', max_length=100, widget=forms.PasswordInput)
 	#email = forms.EmailField(label='Email')

class EditArticleForm(forms.ModelForm):
  class Meta:
    model = Article
    fields = ['title', 'content']

class EditCommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ['comment']


class NewArticleForm(forms.ModelForm):
  class Meta:
    model = Article
    fields = ['title', 'content']

class NewCommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ['comment']

