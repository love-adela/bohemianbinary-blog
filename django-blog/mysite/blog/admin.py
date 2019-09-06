from django.contrib import admin
from .models import Image, Post, Tag
from .forms import PostForm, ImageForm

# Register your models here.
admin.site.register(Post)
admin.site.register(Tag)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    form = ImageForm