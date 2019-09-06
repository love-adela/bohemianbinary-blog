import os
import uuid

from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
import misaka, hoedown, mistune
import logging

from .utils import MarkdownRenderer, FileValidator, RE_FILENAME_IMG


# validators
post_validator = RegexValidator(
    regex='^(?:new|edit|test|preview)*$',
    message="Name is reserved: 'new', 'edit' or 'test'.",
    code='invalid_name',
    inverse_match=True,
)
image_validator = FileValidator(
    restricted_basename=False,
    allowed_extensions=('jpg', 'png', 'svg', 'gif'),
    allowed_mimetypes=('image/jpeg', 'image/png', 'image/svg', 'image/svg+xml', 'image/gif'),
)
image_filename_validator = RegexValidator(
    regex=RE_FILENAME_IMG,
    message="Please use a filename using lowercase letters, digits and underscores. Valid extensions are: 'jpg', 'png', 'svg' or 'gif'",
    code='invalid_name',
    inverse_match=True,
)

def upload_to(model, filename):
    if isinstance(model, Image):
        prefix = 'img/'
    else:
        raise NotImplementedError("upload_to is only implemented for Image models")
    ext = os.path.splitext(filename)[1].lower() # e.g. 'photo.JPG' -> '.jpg'
    filepath = f'{prefix}{uuid.uuid4()}{ext}'
    return filepath
    

class Image(models.Model):
    filename = models.CharField(
        max_length=30, unique=True, blank=False, null=False,
        validators=[post_validator])
    file = models.FileField(
        unique=True, blank=False, null=False, upload_to=upload_to,
        validators=[image_validator])
    
    def __str__(self):
        return self.filename


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


class BaseFormatter:
    def format(self, text):
        pass


class FormatterMisaka(BaseFormatter):

    def format(self, text):
        return misaka.html(text)


class FormatterHoedown(BaseFormatter):
    def format(self, text):
        return hoedown.html(text)


class FormatterMistune(BaseFormatter):
    def format(self, text):
        return mistune.markdown(text)


class Post(models.Model):
    title = models.CharField(max_length=200, help_text='title of message.')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    slug = models.SlugField()
    text = models.TextField(help_text='무슨 생각을 하고 계세요?')
    image = models.ManyToManyField(Image, blank=True)
    # Here are Markdown Parsers
    # formatter = FormatterMisaka()
    # formatter = FormatterHoedown()
    formatter = FormatterMistune()
    draft = models.BooleanField(default=False)
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

    def formatted_text(self):
        logging.error(self.text)
        return self.formatter.format(self.text)
