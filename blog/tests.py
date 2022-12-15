from django.test import TestCase
import os,django,sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
django.setup()
# Create your tests here.
# from blog.models import UserInfo,Tag,Article
# UserInfo.objects.create(username='罗贯中')
# UserInfo.objects.create(username='施耐砌')
# UserInfo.objects.create(username='曹雪芹')
# UserInfo.objects.create(username='吴承恩')
# UserInfo.objects.create(username='龟叔')
# # Tag.objects.create(name='中国')
# # Tag.objects.create(name=' python ')
# topics=['关于猫','关于狗','关于秋月']
# titles=['我是猫','我是狗','我是秋月']
# contents=['我是猫!!!!!!!!','我是狗!!!!!!!!!!!','我是秋月!!!!!!!!!!']
# auths=['猫猫','狗狗','秋月']
# assos=['猫窝','狗窝','秋月窝']
# jours=['猫猫书','狗狗书','秋月书']
# from datetime import datetime, timedelta
# import random
# samples = 30

# start = datetime(1950, 1, 1)
# end = datetime(2020, 1, 1)

# def items(start, end, samples):
#     total_sec = int((end - start).total_seconds())
#     deltas = random.sample(range(total_sec), samples)  # xrange if py2k!
#     return (start + timedelta(seconds=delta) for delta in sorted(deltas))


# haha= list(items(start, end, samples))

# import random
# for i in range (30):
#     Article.objects.create(title=titles[random.randint(0,2)],content=contents[random.randint(0,2)],topic=topics[random.randint(0,2)],auth=auths[random.randint(0,2)],asso=assos[random.randint(0,2)],jour=jours[random.randint(0,2)],date=haha[i])


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
my_text = '太阳很大，你好'
my_query='你好太阳'
highlight = myHighlighter(my_query)
print(highlight.highlight(my_text))