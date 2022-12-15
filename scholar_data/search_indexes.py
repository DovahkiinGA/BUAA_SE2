from haystack import indexes
from .models import *


# ArticleIndex：固定写法 表名Index
class PapersIndex(indexes.SearchIndex, indexes.Indexable):
    # 固定写法  document=True：haystack和搜索引擎，将给text字段分词,建立索引,使用此字段的内容作为索引进行检索
    # use_template=True,使用自己的模板,与document=True进行搭配，自定义检索字段模板(允许谁可以被全文检索,就是谁被建立索引)
    text = indexes.CharField(document=True, use_template=True)
    id = indexes.CharField(model_attr='id')
    title = indexes.CharField(model_attr='title')
    auth = indexes.CharField(model_attr='auth')
    year = indexes.IntegerField(model_attr='year')
    keywords = indexes.CharField(model_attr='keywords')
    fos = indexes.CharField(model_attr='fos')
    n_citation = indexes.IntegerField(model_attr='n_citation')
    references = indexes.CharField(model_attr='references')
    page_stat = indexes.CharField(model_attr='page_stat')
    page_end = indexes.CharField(model_attr='page_end')
    doc_type = indexes.CharField(model_attr='doc_type')
    lang = indexes.CharField(model_attr='lang')
    publisher = indexes.CharField(model_attr='publisher')
    volume = indexes.CharField(model_attr='volume')
    issue = indexes.CharField(model_attr='issue')
    issn = indexes.CharField(model_attr='issn')
    isbn = indexes.CharField(model_attr='isbn')
    doi = indexes.CharField(model_attr='doi')
    pdf = indexes.CharField(model_attr='pdf')
    url = indexes.CharField(model_attr='url')
    abstract = indexes.CharField(model_attr='abstract')
    content_auto = indexes.EdgeNgramField(model_attr='title')
    def get_model(self):
        # 需要建立索引的模型
        return Papers

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        # 写入引擎的数据,必须返回queryset类型
        return self.get_model().objects.all()

class AuthorsIndex(indexes.SearchIndex, indexes.Indexable):
    # 固定写法  document=True：haystack和搜索引擎，将给text字段分词,建立索引,使用此字段的内容作为索引进行检索
    # use_template=True,使用自己的模板,与document=True进行搭配，自定义检索字段模板(允许谁可以被全文检索,就是谁被建立索引)
    text = indexes.CharField(document=True, use_template=True)
    id = indexes.CharField(model_attr='id')
    name = indexes.CharField(model_attr='name')
    normalized_name = indexes.CharField(model_attr='normalized_name')
    orgs = indexes.CharField(model_attr='orgs')
    position = indexes.CharField(model_attr='position')
    n_pubs = indexes.IntegerField(model_attr='n_pubs')
    n_citation = indexes.IntegerField(model_attr='n_citation',null=True)
    tags = indexes.CharField(model_attr='tags')
    pubs = indexes.CharField(model_attr='pubs')
    is_claimed = indexes.IntegerField(model_attr='is_claimed')

    def get_model(self):
        # 需要建立索引的模型
        return Authors

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        # 写入引擎的数据,必须返回queryset类型
        return self.get_model().objects.all()

class VenuesIndex(indexes.SearchIndex, indexes.Indexable):
    # 固定写法  document=True：haystack和搜索引擎，将给text字段分词,建立索引,使用此字段的内容作为索引进行检索
    # use_template=True,使用自己的模板,与document=True进行搭配，自定义检索字段模板(允许谁可以被全文检索,就是谁被建立索引)
    text = indexes.CharField(document=True, use_template=True)
    id = indexes.CharField(model_attr='id')
    DisplayName = indexes.CharField(model_attr='DisplayName')
    NormalizedName = indexes.CharField(model_attr='NormalizedName')
    def get_model(self):
        # 需要建立索引的模型
        return Venues

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        # 写入引擎的数据,必须返回queryset类型
        return self.get_model().objects.all()
  