from django import forms
from django.forms import CheckboxSelectMultiple

from .models import Post, Comment, Image


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['id']
        widgets = {
            # 'tags': CheckboxSelectMultiple(),
            'images': CheckboxSelectMultiple(),
        }
        fields = ('title', 'text',)


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['file']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)
