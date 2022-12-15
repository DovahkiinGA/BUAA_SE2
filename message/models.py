from django.db import models


# Create your models here.

class Message(models.Model):
    senderID = models.IntegerField(verbose_name="发送者的ID")
    receiverID = models.IntegerField(verbose_name="接收者ID", null=False)
    viewed = models.BooleanField(verbose_name="是否查看过了", default=False)
    content = models.TextField(verbose_name="消息内容", null=False)
    type = models.IntegerField(verbose_name="消息种类", null=False)
    postID = models.IntegerField(verbose_name="动态ID",null=True)
    # 1 系统通知，2 私信，3 回复，4 举报成功，5 举报失败，6 申请成功，7 申请失败，8 动态被举报，9 门户被举报
    # 系统ID=0     C
    sendTime = models.DateTimeField(auto_now_add=True)
