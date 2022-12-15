from haystack import indexes
from .models import *
 
 
# ArticleIndex：固定写法 表名Index
class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    # 固定写法  document=True：haystack和搜索引擎，将给text字段分词,建立索引,使用此字段的内容作为索引进行检索
    # use_template=True,使用自己的模板,与document=True进行搭配，自定义检索字段模板(允许谁可以被全文检索,就是谁被建立索引)
    text = indexes.CharField(document=True, use_template=True)
    # 以下字段作为辅助数据,便于调用,最后也不知道怎么辅助,我注释了,也不影响搜索
    # title：写入引擎的字段名,model_attr='title'：相对应的表模型字段名，
    title = indexes.CharField(model_attr='title')
    content = indexes.CharField(model_attr='content')
    topic = indexes.CharField(model_attr='topic')
    auth = indexes.CharField(model_attr='auth')
    asso = indexes.CharField(model_attr='asso')
    jour = indexes.CharField(model_attr='jour')
    date = indexes.CharField(model_attr='date')
 
    def get_model(self):
        # 需要建立索引的模型
        return Article
 
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        # 写入引擎的数据,必须返回queryset类型
        return self.get_model().objects.all()









class UserInfoIndex(indexes.SearchIndex, indexes.Indexable):
    # 固定写法  document=True：haystack和搜索引擎，将给text字段分词,建立索引,使用此字段的内容作为索引进行检索
    # use_template=True,使用自己的模板,与document=True进行搭配，自定义检索字段模板(允许谁可以被全文检索,就是谁被建立索引)
    text = indexes.CharField(document=True, use_template=True)
    # 以下字段作为辅助数据,便于调用,最后也不知道怎么辅助,我注释了,也不影响搜索
    # title：写入引擎的字段名,model_attr='title'：相对应的表模型字段名，
    username = indexes.CharField(model_attr='username')
 
    def get_model(self):
        # 需要建立索引的模型
        return UserInfo
 
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        # 写入引擎的数据,必须返回queryset类型
        return self.get_model().objects.all()