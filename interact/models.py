from django.db import models


# Create your models here.
class CommentOnPost(models.Model):
    postID = models.IntegerField(verbose_name="评论的动态的ID", null=False)
    content = models.TextField(verbose_name="评论内容", null=False)
    userID = models.IntegerField(verbose_name="评论人ID", null=False)
    commentTime = models.DateTimeField(auto_now_add=True)
    floor = models.IntegerField(verbose_name="楼层", null=False, default=1)


class CommentOnLiterature(models.Model):
    literatureID = models.CharField(verbose_name="评论的文献的ID", null=False, max_length=225)
    content = models.TextField(verbose_name="评论内容", null=False)
    userID = models.IntegerField(verbose_name="评论人ID", null=False)
    commentTime = models.DateTimeField(auto_now_add=True)
    floor = models.IntegerField(verbose_name="楼层", null=False, default=1)


class Collection(models.Model):
    userID = models.IntegerField(verbose_name="收藏人ID", null=False)
    literatureID = models.CharField(verbose_name="收藏文献ID", max_length=225)
    collectTime = models.DateTimeField(auto_now_add=True, verbose_name="收藏时间")


class Follow(models.Model):
    followeeID = models.IntegerField(verbose_name="被关注者ID")
    followerID = models.IntegerField(verbose_name="关注者ID")
    followTime = models.DateTimeField(auto_now_add=True)


class Apply(models.Model):
    userID = models.IntegerField(verbose_name="被关注者ID")
    authorID = models.CharField(verbose_name="申请的门户ID",max_length=255)
    email = models.CharField(max_length=100, verbose_name="申请填写的邮箱")  # 看起来没有必要了
    content = models.TextField(verbose_name="申请备注")
    status = models.IntegerField(verbose_name="申请状态", default=0)
    # 0未处理，1接受，2拒绝
    realName = models.TextField(verbose_name="门户名")  # 看起来没有必要了
    applyTime = models.DateTimeField(auto_now_add=True)


class Report(models.Model):
    reporterID = models.IntegerField(verbose_name="举报人ID")
    reporteeID = models.IntegerField(verbose_name="被举报人ID")
    type = models.IntegerField(verbose_name="举报类型")
    # 1举报文献，2举报评论，3举报动态，4举报门户
    objectID = models.CharField(verbose_name="被举报对象ID",max_length=255)
    # 举报对象ID，与上述类型相关
    result = models.IntegerField(verbose_name="处理结果",default=0)
    # 0未处理，1通过，2为通过

    content = models.TextField(verbose_name="举报内容")
    reportTime = models.DateTimeField(auto_now_add=True)


class FollowSector(models.Model):
    userID = models.IntegerField(verbose_name="用户ID", null=False)
    sectorID = models.IntegerField(verbose_name="分区ID", null=False)
    followTime = models.DateTimeField(auto_now_add=True)
