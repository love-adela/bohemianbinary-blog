from django.db import models
from django.utils import timezone
from django.utils.html import mark_safe
from django.urls import reverse_lazy
import misaka, hoedown, mistune
import logging

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
    

class BaseFormatter:
    def format(self, text):
        pass

class FormatterMisaka(BaseFormatter):
    
    def format(self, text):
        return misaka.html(text)

class FormatterHoedown(BaseFormatter):
    def format(self, text):
        return hoedown.html(text)

class FormatterMistune(BaseFormatter):
    def format(self, text):
        return mistune.markdown(text)

class Post(models.Model):
    title = models.CharField(max_length=200, help_text='title of message.')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    slug = models.SlugField()
    text = models.TextField(help_text='무슨 생각을 하고 계세요?')
    # Here are Markdown Parsers
    # formatter = FormatterMisaka()
    # formatter = FormatterHoedown()
    formatter = FormatterMistune()
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

    def formatted_text(self):
        logging.error(self.text)
        return self.formatter.format(self.text)