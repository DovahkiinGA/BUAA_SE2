from django.db import models


# Create your models here.

class Post(models.Model):
    referenceDocID = models.CharField(verbose_name="引用文献的ID",max_length=225)
    postContent = models.TextField(verbose_name="动态内容")
    posterID = models.IntegerField(verbose_name="动态发布者ID")
    postTime = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=255)
    floors = models.IntegerField(verbose_name="评论楼数", default=1)
    sectorID = models.IntegerField(verbose_name="动态所属分区ID", null=False)

    def set_tags(self, tags):
        # Serialize the array
        self.tags = ','.join(tags)

    def get_tags(self):
        # Deserialize the array
        return self.tags.split(',')
