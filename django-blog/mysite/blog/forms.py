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

    def clean(self):
        """ Checks whether set(linked files) == set(referenced files) """
        linked_images = {img.filename for img in self.cleaned_data['images']}
        referenced_images = {m['filename'] for m in RE_MARKDOWN_IMG.finditer(self.cleaned_data.get('markdown', ''))}
        missing_files = referenced_images - linked_images
        superfluous_files = linked_images - referenced_images
        if missing_files:
            raise ValidationError(
                "Please upload/link these missing image files referenced in "
                "the markdown text: " + ", ".join(missing_files))
        if superfluous_files:
            raise ValidationError(
                "Please delete/unlink these non-referenced image files in "
                "the markdown text: " + ", ".join(superfluous_files))
        return self.cleaned_data


class ImageForm(ModelForm):
    class Meta:
        model = Image
        exclude = ['id']

    def clean(self):
        purported_ext = os.path.splitext(self.cleaned_data['filename'])[1][1:]
        actual_ext = os.path.splitext(self.cleaned_data['file'].name)[1][1:]
        logging.error(purported_ext)
        logging.error(actual_ext)
        if purported_ext != actual_ext:
            raise ValidationError(
                "Filename extension must match uploaded file: '{ext}'"
                    .format(ext=actual_ext))
        return self.cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)
