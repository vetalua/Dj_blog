# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
	
	class Meta():
		db_table = 'article'

	article_title = models.CharField(max_length = 200)
	article_text = models.TextField()
	article_likes = models.IntegerField(default=0)
	article_date = models.DateTimeField()


class Comments(models.Model):

	class Meta():
		db_table = 'comments'

	comments_text = models.TextField(verbose_name='Comments text')
	comments_article = models.ForeignKey(Article)
	comments_date = models.DateTimeField()
	comments_from = models.ForeignKey(User)