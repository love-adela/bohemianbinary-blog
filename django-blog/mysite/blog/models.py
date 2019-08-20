from django.db import models
from django.utils import timezone
from django.utils.html import mark_safe
from django.urls import reverse_lazy
from markdown import markdown


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
    draft  = models.BooleanField(default=False)
    
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
    
    def get_text_as_markdown(self):
        return mark_safe(markdown(self.text, safe_mode='escape'))