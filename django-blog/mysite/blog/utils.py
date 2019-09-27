# import houdini
import misaka, hoedown, mistune
import mimetypes
import os
import re

from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _

from pygments import highlight
from pygments.formatters import HtmlFormatter, ClassNotFound
from pygments.lexers import get_lexer_by_name
import logging

RE_FILENAME_IMG = re.compile(r'[a-z0-9\_]+\.(?:jpg|png|svg|gif)')
RE_MARKDOWN_IMG = re.compile(r'(?P<full>\!\[(?P<alt>.*)\]\((?P<filename>' + RE_FILENAME_IMG.pattern + r')\))')


class MarkdownRenderer:
    def __init__(self, post_model_obj=None):
        self.post = post_model_obj

    def image_html(self, image_model_obj):
        filepath = os.path.join(settings.MEDIA_URL, image_model_obj.file.name)
        return (
            '<figure id="{filename}">'
            '<img class="post_image" src="{filepath}" alt="{filename}"/>'
            '<figcaption>'
            '<span class="figcaption_prefix">Figure: </span>{{caption}}'
            '</figcaption>'
            '</figure>'
                .format(
                filename=image_model_obj.filename,
                filepath=filepath))

    def render(self, markdown):
        if self.post is not None and self.post.id is not None:
            image_html = {img.filename: self.image_html(img) for img in self.post.images.all()}
            translate = {m['full']: image_html.get(m['filename'], "[IMAGE NOT FOUND]").format(caption=m['alt']) for m in
                         RE_MARKDOWN_IMG.finditer(markdown)}
            for orig, repl in translate.items():
                markdown = markdown.replace(orig, repl)
        html = mistune.html(markdown)
        return html


class HighlighterRenderer(misaka.HtmlRenderer):
    def blockcode(self, text, lang):
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except ClassNotFound:
            lexer = None
        if lexer:
            formatter = HtmlFormatter(cssclass="highlight")
            return highlight(text, lexer, formatter)
        return f'\n<pre><code>{houdini.escape_html(text.strip())}</code></pre>\n'


class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            return f'\n<pre><code>%{mistune.escape(code)}</code></pre>\n'

        if lang:
            try:
                lexer = get_lexer_by_name(lang, stripall=True)
            except ClassNotFound:
                code = lang + '\n' + code
                lang = None

        formatter = HtmlFormatter(cssclass="highlight")
        return highlight(code, lexer, formatter)


class BaseFormatter:
    def format(self, text):
        pass


class FormatterMisaka(BaseFormatter):
    def format(self, text):
        renderer = HighlighterRenderer()
        markdown = misaka.Markdown(renderer, extensions=('fenced-code',))
        return markdown(text)


# class FormatterHoedown(BaseFormatter):
#     def format(self, text):
#         return hoedown.html(text)


class FormatterMistune(BaseFormatter):
    def format(self, text):
        renderer = HighlightRenderer()
        markdown = mistune.Markdown(renderer=renderer)
        return markdown(text)


@deconstructible
class FileValidator:
    RE_BASENAME = re.compile(r'[a-z0-9\_]+')

    # Error messages
    basename_message = _(
        "Basename '%(basename)s' contains bad characters. Allowed characters are lowercase letters, digits and underscores.")
    extension_message = _("Extension '%(extension)s' not allowed. Allowed extensions are: '%(allowed_extensions)s.'")
    mime_message = _("MIME type '%(mimetype)s' is not valid. Allowed types are: %(allowed_mimetypes)s.")
    min_size_message = _('The current file %(size)s, which is too small. The minumum file size is %(allowed_size)s.')
    max_size_message = _('The current file %(size)s, which is too large. The maximum file size is %(allowed_size)s.')

    def __init__(self, *args, **kwargs):
        self.restricted_basename = kwargs.pop('restricted_basename', True)
        self.allowed_extensions = kwargs.pop('allowed_extensions', None)
        self.allowed_mimetypes = kwargs.pop('allowed_mimetypes', None)
        self.min_size = kwargs.pop('min_size', 0)
        self.max_size = kwargs.pop('max_size', None)

    def __call__(self, value):
        """
        Check the extension, content type and file size.
        """
        basename, ext = os.path.splitext(value.name)
        ext = ext[1:].lower()

        # Check the basename
        if self.restricted_basename and not self.RE_BASENAME.match(basename):
            message = self.basename_message % {'basename': basename}
            raise ValidationError(message)

        # Check the extension
        if self.allowed_extensions and ext not in self.allowed_extensions:
            message = self.extension_message % {
                'extension': ext,
                'allowed_extensions': ', '.join(self.allowed_extensions)
            }
            raise ValidationError(message)

        # Check the content type
        mimetype = mimetypes.guess_type(value.name)[0]
        if self.allowed_mimetypes and mimetype not in self.allowed_mimetypes:
            message = self.mime_message % {
                'mimetype': mimetype,
                'allowed_mimetypes': ', '.join(self.allowed_mimetypes)
            }
            raise ValidationError(message)

        filesize = len(value)
        if self.max_size and filesize > self.max_size:
            message = self.max_size_message % {
                'size': filesizeformat(filesize),
                'allowed_size': filesizeformat(self.max_size)
            }
            raise ValidationError(message)

        elif filesize < self.min_size:
            message = self.min_size_message % {
                'size': filesizeformat(filesize),
                'allowed_size': filesizeformat(self.min_size)
            }
            raise ValidationError(message)
