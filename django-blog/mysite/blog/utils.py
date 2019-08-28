import misaka, hoedown, mistune

class BaseFormatter:
    def format(self, text):
        pass


class FormatterMisaka(BaseFormatter):
    def format(self, text):
        return misaka.html(text, extensions=['math', 'math-explicit', 'fenced-code', 'footnotes'], render_flags=[])


class FormatterHoedown(BaseFormatter):
    def format(self, text):
        return hoedown.html(text)


class FormatterMistune(BaseFormatter):
    def format(self, text):
        return mistune.markdown(text)
