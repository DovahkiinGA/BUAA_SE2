from django.db import models
 
 
class UserInfo(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=225)
 
    def __str__(self):
        return self.username
 
 
class Tag(models.Model):
    name = models.CharField(verbose_name='标签名称', max_length=225)
 
    def __str__(self):
        return self.name
 
 
class Article(models.Model):
    topic = models.CharField(verbose_name='主题', max_length=225)
    title = models.CharField(verbose_name='标题', max_length=225)
    content = models.TextField(verbose_name='内容', max_length=225)
    # 外键
    #username = models.ForeignKey(verbose_name='作者', to='UserInfo', on_delete=models.DO_NOTHING)
    #tag = models.ForeignKey(verbose_name='关键词', to='Tag', on_delete=models.DO_NOTHING)
    auth = models.CharField(verbose_name='作者', max_length=225)
    asso = models.CharField(verbose_name='组织', max_length=225)
    jour = models.CharField(verbose_name='期刊', max_length=225)
    date = models.DateField(verbose_name='日期')
    def __str__(self):
        return self.title