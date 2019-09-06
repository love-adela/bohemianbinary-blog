import houdini 
import misaka, hoedown, mistune
# from misaka import Markdown, HtmlRenderer
from pygments import highlight
from pygments.formatters import HtmlFormatter, ClassNotFound
from pygments.lexers import get_lexer_by_name
import logging


# class HighlighterRenderer(misaka.HtmlRenderer):
#     def highlight_code(self, text, lang):
#         try:
#             lexer = get_lexer_by_name(lang, stripall=True)
#         except ClassNotFound:
#             lexer = None
#         if lexer:
#             formatter = HtmlFormatter(cssclass="highlight")
#             return highlight(text, lexer, formatter)
#         return f'\n<pre><code>{houdini.escape_html(text.strip())}</code></pre>\n'


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


# class FormatterMisaka(BaseFormatter):
#     def format(self, text):
#         renderer = HighlighterRenderer()
#         markdown = misaka.Markdown(renderer, extensions=('fenced-code',))
#         return markdown(text)


# class FormatterHoedown(BaseFormatter):
#     def format(self, text):
#         return hoedown.html(text)


class FormatterMistune(BaseFormatter):
    def format(self, text):
        renderer = HighlightRenderer()
        markdown = mistune.Markdown(renderer=renderer)
        return markdown(text)
