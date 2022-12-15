from haystack.utils.highlighting import Highlighter
"""
自定义关键词高亮器，不截断过短的文本（例如文章标题）
"""
from django.utils.html import strip_tags
from haystack.utils import Highlighter as HaystackHighlighter

class myHighlighter(HaystackHighlighter):
    def highlight(self, text_block):
        self.text_block = strip_tags(text_block)
        highlight_locations = self.find_highlightable_words()
        start_offset, end_offset = self.find_window(highlight_locations)
        if len(text_block) < self.max_length:
            start_offset = 0
        return self.render_html(highlight_locations, start_offset, end_offset)
# my_text = 'This is a sample block that would be more meaningful in real life.'
# my_query = 'block meaningful'
# my_text = '太阳很大，你好'
# my_query='你好太阳'
# highlight = myHighlighter(my_query)
# print(highlight.highlight(my_text))