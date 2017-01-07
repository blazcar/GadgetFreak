from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User

import sys

from .forms import LoginForm, UserForm



def index(request):
	return render(request, 'index.html')

def login_user(request):
  context = {'LoginForm':LoginForm()}
  if request.method=='POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
      if user is not None:
        login(request, user)
    return HttpResponseRedirect(reverse('index'))
  else:
    form = LoginForm()
  context['LoginForm'] = form
  return render(request, 'login.html', context)


def register_user(request):
	context = {'UserForm':UserForm()}
	if request.method == 'POST':
		uf = UserForm(request.POST)
		if uf.is_valid():
		  User.objects.create_user(username=uf.cleaned_data['username'],password=uf.cleaned_data['password'])
		return HttpResponseRedirect(reverse('index'))
	else: 
		uf = UserForm()
	context['UserForm'] = uf
	return render(request, 'register.html', context)


	

def logout_user(request):
  logout(request)
  return HttpResponseRedirect(reverse('index'))
