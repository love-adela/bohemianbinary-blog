from django.db import models
from django.utils import timezone
# from .utils import FormatterMisaka
from .utils import FormatterMistune
import logging

try:
    from unicode import unicode
except ImportError:

    def unicode(tag):
        return tag


class Tag(models.Model):
    text = models.CharField(max_length=250)
    # slug = models.SlugField(unique=True, max_length=200)
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ('created_date',)

    # def __str__(self):
    #     return self.slug

    def get_absolute_url(self):
        pass

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

    # TODO : get_absolute_url() 만들기
    # def get_absolute_url(self):
    #   return f"/{self.published_date.year}/{self.published_date.month}/{self.slug}"

    def formatted_text(self):
        return self.formatter.format(self.text)
    
    def approved_comments(self):
        return self.comments.filter(approved_comment=True)    

    
class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    
    def approve(self):
        self.approved_comment = True
        self.save()
        
    def __str__(self):
        return self.text