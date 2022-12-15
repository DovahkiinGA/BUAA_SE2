from django.db import models


# Create your models here.
class Papers(models.Model):
    id = models.CharField(verbose_name='id', max_length=225,primary_key = True)
    title = models.CharField(verbose_name='标题', max_length=1000,default="")
    auth = models.CharField(verbose_name='作者信息', max_length=1000,default="")
    year = models.IntegerField(verbose_name='日期',default=1900)
    keywords = models.CharField(verbose_name='关键词', max_length=1000,default="")
    fos = models.CharField(verbose_name='领域', max_length=1000,default="")
    n_citation = models.IntegerField(verbose_name='引用次数',default=0)
    references = models.CharField(verbose_name='引用文章', max_length=1000,default="")
    page_stat = models.CharField(verbose_name='开始页数', max_length=500,default="")
    page_end = models.CharField(verbose_name='结束页数', max_length=500,default="")
    doc_type = models.CharField(verbose_name='文章类型', max_length=500,default="")
    lang = models.CharField(verbose_name='语言', max_length=225,default="")
    publisher = models.CharField(verbose_name='出版商', max_length=1000,default="")
    volume = models.CharField(verbose_name='volume', max_length=1000,default="")
    issue = models.CharField(verbose_name='期号', max_length=225,default="")
    issn = models.CharField(verbose_name='issn', max_length=225,default="")
    isbn = models.CharField(verbose_name='isbn', max_length=225,default="")
    doi = models.CharField(verbose_name='doi', max_length=255,default="")
    pdf = models.CharField(verbose_name='pdf链接', max_length=1000,default="")
    url = models.CharField(verbose_name='链接', max_length=1000,default="")
    abstract = models.CharField(verbose_name='摘要', max_length=1000,default="")

    def __str__(self):
        return self.title


class Venues(models.Model):
    id = models.CharField(verbose_name='id', max_length=225,primary_key = True)
    DisplayName = models.CharField(verbose_name='缩写', max_length=1000,default="")
    NormalizedName = models.CharField(verbose_name='全名', max_length=1000,default="")

    def __str__(self):
        return self.DisplayName


class Authors(models.Model):
    id = models.CharField(verbose_name='id', max_length=225,primary_key = True)
    name = models.CharField(verbose_name='名字', max_length=1000,default="")
    normalized_name = models.CharField(verbose_name='标准名字', max_length=1000,default="")
    orgs = models.CharField(verbose_name='所属机构', max_length=1000,default="")
    position = models.CharField(verbose_name='职级', max_length=1000,default="")
    n_pubs = models.IntegerField(verbose_name='文章数',default=0)
    n_citation = models.IntegerField(verbose_name='被引数',default=0)
    tags = models.CharField(verbose_name='研究领域', max_length=1000,default="")
    #t:research interests,i:weight of interests
    #"tags": [{"w": 1, "t": "Vehicle Theft .Immobilisation .Crime Prevention.Crimereduction . Displacement .Motorcycle Theft .Opportunistic Offenders .Professional Offenders . Evaluation.Mixed-Methods Design"}]
    pubs = models.CharField(verbose_name='论文id', max_length=2000,default="")
    #{"i": "53e9bc79b7602d97048f8888", "r": 2}
    is_claimed = models.IntegerField(verbose_name='是否认领', default = 0)

    def __str__(self):
        return self.name


class DownloadandSearch(models.Model):

    download = models.IntegerField(verbose_name='下载',default=0)
    search = models.IntegerField(verbose_name='搜索',default=0)


