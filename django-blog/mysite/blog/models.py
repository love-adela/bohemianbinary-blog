from django.db import models
from django.utils import timezone
from django.urls import reverse_lazy

try:
    from unicode import unicode
except ImportError:

    def unicode(tag):
        return tag


class Tag(models.Model):
    text = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, max_length=200)
    created_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ('created_date',)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        pass

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    text = models.TextField()

    draft  = models.BooleanField(default=False)
    # image = models.ImageField(upload_to="", null=True, blank=True)
    
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
