import os
import uuid

from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

# from .utils import MarkdownRenderer
from .utils import FileValidator, RE_FILENAME_IMG
# from .utils import FormatterMisaka
from .utils import FormatterMistune

import logging

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
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        null=True,
    )
    file = models.FileField(
        unique=True, blank=False, null=False, upload_to=upload_to,
        validators=[image_validator])

    def __str__(self):
        return self.file.path


try:
    from unicode import unicode
except ImportError:

    def unicode(tag):
        return tag


class Tag(models.Model):
    title = models.CharField(
        max_length=30, unique=True, null=False)

    def __str__(self):
        return self.title


class PostQuerySet(models.QuerySet):
    def posts(self):
        return self.filter(published_date__lte=timezone.now()).order_by('-published_date')
    
    def detail_post(self, post_id):
        return self.filter(uuid=post_id).first()
    
    def drafts(self):
        return self.filter(draft=True).order_by('-created_date')


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)
    
    def posts(self):
        return self.get_queryset().posts()
    
    def detail_post(self, post_id):
        return self.get_queryset().detail_post(post_id)

    def drafts(self):
        return self.get_queryset().drafts()
    
    

class Post(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE,)
    last_contributor = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                                        null=True, related_name='last_contributor')
    title = models.CharField(max_length=200, help_text='제목을 입력하세요.')
    text = models.TextField(help_text='무슨 생각을 하고 계세요?')
    # Here are Markdown Parsers
    # formatter = FormatterMisaka()
    # formatter = FormatterHoedown()
    formatter = FormatterMistune()
    draft = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    objects = PostManager()
    

    class Meta:
        ordering = ['-published_date', ]

    def __str__(self):
        return self.title

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # TODO : get_absolute_url() 만들기
    # def get_absolute_url(self):
    #   return f"/{self.published_date.year}/{self.published_date.month}/{self.slug}"

    def formatted_text(self):
        return self.formatter.format(self.text)

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


class RevisionQuerySet(models.QuerySet):
    def revisions(self, post):
        return self.filter(post=post)

    def recent_ordered_revisions(self, post):
        return self.revisions(post).order_by('-created_date')

    def current_revision(self, post, revision_id):
        return self.revisions(post).filter(revision_id=revision_id).first()

    def previous_revision(self, post, current):
        return self.revisions(post).filter(created_date__lt=current.created_date).filter().order_by('-created_date').first()


class RevisionManager(models.Manager):
    def get_queryset(self):
        return RevisionQuerySet(self.model, using=self._db)
    
    def revisions(self, post):
        return self.get_queryset().revisions(post) 

    def recent_ordered_revisions(self, post):
        return self.get_queryset().recent_ordered_revisions(post)
    
    def current_revision(self, post, revision_id):
        return self.get_queryset().current_revision(post, revision_id)

    def previous_revision(self, post, current):
        return self.get_queryset().previous_revision(post, current)

class Revision(models.Model):
    revision_id = models.IntegerField(default=1)
    post = models.ForeignKey('blog.Post',
                            on_delete=models.CASCADE, related_name='revisions')
    title = models.CharField(max_length=200, help_text='제목을 입력하세요', null=True) 
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    objects = RevisionManager()

    def __str__(self):
        return self.text
