import houdini 
import misaka, hoedown, mistune

from pygments import highlight
from pygments.formatters import HtmlFormatter, ClassNotFound
from pygments.lexers import get_lexer_by_name

class BaseFormatter:
    def format(self, text):
        pass


class FormatterMisaka(BaseFormatter):
    def format(self, text):
        return misaka.html(renderer, extensions=['math', 'math-explicit', 'fenced-code', 'footnotes'], render_flags=[])


class FormatterHoedown(BaseFormatter):
    def format(self, text):
        return hoedown.html(text)


class FormatterMistune(BaseFormatter):
    def format(self, text):
        return mistune.markdown(text)


class HighlighterRenderer(misaka.HtmlRenderer):
    def blockcode(self, text, lang):
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except ClassNotFound:
            lexer = None
        
        if lexer:
            formatter = HtmlFormatter()
            return highlight(text, lexer, formatter)

        return (f'\n<pre><code>{houdini.escape_html(text.strip())}</code></pre>\n')

renderer = HighlighterRenderer()
