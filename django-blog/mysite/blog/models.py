from django.db import models
from django.utils import timezone
from django.utils.html import mark_safe
from markdownx.models import MarkdownxField

try:
    from unicode import unicode
except ImportError:

    def unicode(tag):
        return tag


class Tag(models.Model):
    text = models.CharField(max_length=250)
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ('created_date',)

    def get_absolute_url(self):
        pass
    

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    slug = models.SlugField()
    text = models.TextField()
    draft = models.BooleanField(default=False)
    tag = models.ManyToManyField(Tag)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ['-published_date',]

    def __str__(self):
        return self.title

    def publish(self):
        self.published_date = timezone.now()
        self.save()


class BaseFormatter:
    def __init__(self, post):
        self.post = post

    def format(self):
        return BaseFormatter.format(self.post.text)

class FormatterA(BaseFormatter):
    formatter = MarkdownxField()

# Todo : markdown() 라이브러리 추가
# class FormatterB(BaseFormatter):
#     formatter = FormatterBLib

