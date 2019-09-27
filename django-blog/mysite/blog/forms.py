from django import forms
from django.forms import ModelForm, CheckboxSelectMultiple

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
        exclude = ['id']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)
