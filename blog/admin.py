from django.contrib import admin
from .models import Image, Comment, Post, Tag

# Register your models here.
admin.site.register(Comment)
admin.site.register(Tag)


class ImageAdmin(admin.StackedInline):
    model = Image


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['title']}), )
    inlines = [ImageAdmin, ]
