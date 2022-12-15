from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=128, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=256)
    has_confirmed = models.BooleanField(default=False)
    avatar = models.CharField(max_length=1024, default='')
    brief_intro = models.CharField(max_length=1024, default='')
    tel = models.CharField(max_length=18, default="")
    gender = models.IntegerField(default=0)
    nickname = models.CharField(max_length=128, default="")

    phoneNumber = models.CharField(max_length=20, verbose_name="手机号", default="")
    organization = models.CharField(max_length=50, verbose_name="所属组织", default="")
    realName = models.CharField(max_length=50, verbose_name="真名", default="")
    userDegree = models.IntegerField(default=0, verbose_name="用户学位，0到3分别为本科以下，本科，硕士，博士")

    isAdministrator=models.BooleanField(default=False)
    #增加了是否为管理员的标签，默认为否，通过管理员创建api创建的用户为真
    authorID = models.CharField(verbose_name='认领门户id', max_length=225)
    # todo:authorID改为models.CharField(verbose_name='id', max_length=225)
    def __str__(self):
        return self.username


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ":" + self.code

    class Meta:
        db_table = 'tb_confirmCode'
        ordering = ['-c_time']
        verbose_name = '确认码'
        verbose_name_plural = verbose_name
