import os

from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CheckboxSelectMultiple

from .models import Post, Comment, Image
from .utils import RE_MARKDOWN_IMG

import logging


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['id']
        widgets = {
            # 'tags': CheckboxSelectMultiple(),
            'images': CheckboxSelectMultiple(),
        }
        fields = ('title', 'text',)


class ImageForm(ModelForm):
    class Meta:
        model = Image
        exclude = ['id']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)
