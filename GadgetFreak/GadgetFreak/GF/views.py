from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from .models import Article, Comment
from django.template import loader
from django.http import HttpResponse
from .forms import EditArticleForm, EditCommentForm, NewArticleForm, NewCommentForm, LoginForm, UserForm
import sys
import logging

logger = logging.getLogger('apps')


def write_comment(request, article_id):
	"""Funtion to write comment to article

	This function allows user to comment the article with id of article_id
	
	Keyword arguments:
		request -- the django request object
		article_id -- the id of the article to comment
	"""		
	if request.method == 'POST':
		form = NewCommentForm(request.POST)
		# checks if form is valid
		if form.is_valid():
			comment = form.cleaned_data['comment']
			author = request.user
			article_id = Article.objects.get(id=article_id)
			comment = Comment(comment=comment,author=author, article_id=article_id)
			comment.save()
			logger.info('{ ' + author.username + ' } wrote comment under article ' + article_id.title)
		else:
			logger.warning('Form for writing comment was not valid')
	return HttpResponseRedirect(reverse('index'))



def write_article(request):
	"""Funtion to write new article

	This function allows logged user to write new article.
	
	Keyword arguments:
		request -- the django request object
	"""			
	if(request.method == 'POST'):
		form = NewArticleForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			content = form.cleaned_data['content']
			author = request.user
			article = Article(title=title, content=content, author=author)
			article.save()
			logger.info('{ ' + author.username + ' } wrote article ' + title)
		else:
			logger.warning('Form for writing article was not valid')
	return HttpResponseRedirect(reverse('index'))
				



def index(request):
		"""Landing page

		This is the landing page of application. It contains all articles and comments to the articles.
		
		Keyword arguments:
		request -- the django request object
		"""		
		articles = Article.objects.all()
		comments = Comment.objects.all()
		context = {'articles': articles, 'comments':comments, 'NewArticleForm':NewArticleForm, 'NewCommentForm':NewCommentForm, }	
		template = loader.get_template('index.html')
		return HttpResponse(template.render(context, request))

def login_user(request):
  """Page for user to login

		This is the page with form for login.
		
		Keyword arguments:
		request -- the django request object
  """
  context = {'LoginForm':LoginForm()}
  if request.method=='POST':
    form = LoginForm(request.POST)
		#checks if form is valid
    if form.is_valid():
      user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
			#checks if app can authenticate user
      if user is not None:
        login(request, user)
        logger.info('{ ' + user.username + ' } successfully logged in')
      else:
        logger.error('Authentication of user { ' + user.username + ' } failed' )
    else:
		  logger.warrning('Login form was not valid')
    return HttpResponseRedirect(reverse('index'))
  else:
    form = LoginForm()
  context['LoginForm'] = form
  return render(request, 'login.html', context)


def register_user(request):
	"""Register page

			This is the register page of application. It contains form for user to create account.
		
			Keyword arguments:
			request -- the django request object
			"""
	context = {'UserForm':UserForm()}
	if request.method == 'POST':
		uf = UserForm(request.POST)
		#checks if register form is valid
		if uf.is_valid():
			nov = User.objects.filter(username=uf.cleaned_data['username']).count()
			#checks if user already exists
			if(nov == 0):
				nov = User.objects.create_user(username=uf.cleaned_data['username'],password=uf.cleaned_data['password'])
				nov.save()				
				logger.info('User with username { ' + uf.cleaned_data['username'] + ' } was successfully registered')
			else:
				logger.error('User with username { ' + uf.cleaned_data['username'] + ' } already exists')
		else:	
			logger.warning('Register form was not valid')
		return HttpResponseRedirect(reverse('index'))
	else: 
		uf = UserForm()
	context['UserForm'] = uf
	return render(request, 'register.html', context)


	

def logout_user(request):
  """Function to logout the user
		
		Keyword arguments:
		request -- the django request object
  """
  logout(request)
  logger.info('User with username { ' + request.user.username + ' } logged out')
  return HttpResponseRedirect(reverse('index'))



def article_edit(request, article_id):
  """Page for editing article

		This is the page where user can edit his article. It contains a form to edit the article.
		
		Keyword arguments:
		request -- the django request object
		article_id -- the id of the article to edit.
  """
  context = {'loginForm':LoginForm()}
  article = Article.objects.get(pk=article_id)
  eaform = EditArticleForm(instance=article)
  if request.method == 'GET':
		#check if user that wants to edit article is also the author of that article
    if request.user.username != Article.objects.get(id=article_id).author.username:
      logger.warning('{ ' + request.user.username + ' } is not permitted to edit article ' + article.title)
      return HttpResponseRedirect(reverse('index'))
  
  if request.method=='POST':
    eaform = EditArticleForm(request.POST, instance=article)
		#checks if article edit form is valid
    if eaform.is_valid():
      eaform.save()
      logger.info('User { ' + request.user.username + ' } edited article ' + article.title)
      return HttpResponseRedirect(reverse('index'))
    else:
      logger.warning('Form for editing article is not valid')
      
  context['article'] = article
  context['edit_article_form'] = eaform

  return render(request, 'article_edit.html', context)



def article_view(request, article_id):	
  """Article view page

		This is the page where everyone can see article content. It contains artcile and also all of it's comments
		
		Keyword arguments:
		request -- the django request object
		article_id -- the id of article to view
  """
  context = {'loginForm':LoginForm()}
  
  article = Article.objects.get(pk=article_id)
  context['article'] = article
  
  return render(request, 'article_view.html', context)

def comment_edit(request, comment_id):
  """Page to edit the comment

		This is the page that user can edit his comment. It contains a form to edit the comment.
		
		Keyword arguments:
		request -- the django request object
		comment_id -- the id of the comment to edit
  """
  context = {'loginForm':LoginForm()}
  comment = Comment.objects.get(pk=comment_id)
  ecform = EditCommentForm(instance=comment)
  if request.method == 'GET':
		#checks if user that wants to edit comment is also the author
    if (request.user.username != Comment.objects.get(id=comment_id).author.username):
      logger.warning('{ ' + request.user.username + ' } is not permitted to edit this comment')
      return HttpResponseRedirect(reverse('index'))
  
  if request.method=='POST':
    ecform = EditCommentForm(request.POST, instance=comment)
		#checks if form is valid
    if ecform.is_valid():
      ecform.save()
      logger.info('User { ' + request.user.username + ' } edited comment ')
      return HttpResponseRedirect(reverse('index'))
  else:
    logger.warning('Form for editing comment is not valid')
      
  context['comment'] = comment
  context['edit_comment_form'] = ecform

  return render(request, 'comment_edit.html', context)

def comment_view(request, comment_id):
  """Page to view the comment

		This is the landing page of application. It contains the comment content and also links to edit or delete comment
		
		Keyword arguments:
		request -- the django request object
		comment_id -- id of the comment to view
  """
  context = {'loginForm':LoginForm()}
  
  comment = Comment.objects.get(pk=comment_id)
  context['comment'] = comment
  
  return render(request, 'comment_view.html', context)



def article_delete(request, article_id):
	"""Function to delete the article

		This function deletes article with id article_id
		
		Keyword arguments:
		request -- the django request object
		article_id -- id of the article to delete
		"""
	a = Article.objects.get(id=article_id)
	#checks if user is allowed to delete the article (is author of it)
	if request.user.username == a.author.username:
		a.delete()
		logger.info('Article ' + a.title + ' was successfully deleted')
		return HttpResponseRedirect(reverse('index'))
	else:
		logger.error('User { ' + request.user.username + ' } is not permitted to delete article '+ a.title)
	return article_view(request, article_id)

def comment_delete(request, comment_id):
	"""Function to delete the comment

		This function deletes comment with id comment_id
		
		Keyword arguments:
		request -- the django request object
		comment_id -- id of the comment to delete
		"""
	c = Comment.objects.get(id=comment_id)
	#checks if user is allowed to delete the article (is author of it)
	if request.user.username == c.author.username:
		c.delete()
		logger.info('Comment was successfully deleted')
		return HttpResponseRedirect(reverse('index'))
	else:
		logger.error('User { ' + request.user.username + ' } is not permitted to delete this comment')
	return comment_view(request, comment_id)

























