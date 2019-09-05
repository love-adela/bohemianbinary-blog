from django.contrib import admin
from .models import Comment, Post, Tag

# Register your models here.
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Tag)