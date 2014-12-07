from django.shortcuts import render
from django.http.response import HttpResponse, Http404
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response, redirect
from article.models import Article, Comments
from django.core.exceptions import ObjectDoesNotExist
from forms import CommentForm
from django.core.context_processors import csrf
from django.core.paginator import Paginator
from django.contrib import auth
import datetime

# Create your views here.
def basic_one(request):
	view = 'basic_one'
	html = "<html><body> This is %s view </body></html>" % view
	return HttpResponse(html)

def template_two(request):
	view = 'template_two'
	t = get_template('myview.html')
	html = t.render(Context({'name': view}))
	return HttpResponse(html)

def template_three_simple(request):
	view = 'template_three'
	return render_to_response('myview.html',{'name': view})

def articles (request, page_number=1):
	all_articles = Article.objects.all()
	#all_articles = reverse(al_articles) # reverse not work !!!
	#print len(all_articles)
	print all_articles
	current_page = Paginator(all_articles, 2)
	return render_to_response('articles.html', {'articles':current_page.page(page_number),'username' : auth.get_user(request).username, 'page_number' : page_number})

#def article(request, article_id = 1):
#	return render_to_response('article.html', {'article' : Article.objects.get(id = article_id), 'comments' : Comments.objects.filter(comments_article_id = article_id)})

def article(request, article_id = 1):
	print 'start article view'
	comment_form = CommentForm
	args = {}
	args.update(csrf(request))
	args['article'] = Article.objects.get(id = article_id)
	args['comments'] = Comments.objects.filter(comments_article_id = article_id)
	#all_comments = Comments.objects.filter(comments_article_id = article_id)#
	#currents_subpage = Paginator(all_comments, 3)
	#args['comments'] = currents_subpage.page(comments_subpage) # 43 - 47 add 2.12.2014
	args['form'] = comment_form
	args['username'] = auth.get_user(request).username
	print 'end article view'
	return render_to_response('article.html', args)

def addlike(request, article_id, page_number=1):
	print 'add like view', page_number
	try:
		if article_id in request.COOKIES:
			redirect('/page/%s/' % page_number)
		else:
			article = Article.objects.get(id = article_id)
			article.article_likes += 1
			article.save()
			response = redirect('/page/%s/' % page_number)					# create Cookie
			response.set_cookie(article_id, ' %s is the current_page of application. Do with it all you want ' % page_number)	# create Cookie
			return response
	except ObjectDoesNotExist:
		raise Http404
	return redirect('/page/%s/' % page_number)

def addcomment(request, article_id):
	if request.POST and ('pause' not in request.session):
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.comments_article = Article.objects.get(id = article_id)
			comment.comments_date = datetime.datetime.now()
			comment.comments_from = auth.get_user(request)
			form.save()
			request.session.set_expiry(60)		# SESSION 60 sec
			request.session['pause'] = True		# SESSION
	return redirect('/articles/get/%s/' % article_id)