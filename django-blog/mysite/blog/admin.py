from django.contrib import admin
from .models import Image, Comment, Post, Tag
from .forms import ImageForm

# Register your models here.
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Tag)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    form = ImageForm
