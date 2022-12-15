from django.db import models


# Create your models here.
class Sector(models.Model):
    name = models.TextField(verbose_name="分区名")
    counter = models.IntegerField(default=0, verbose_name="分区内动态数")
    tags = models.CharField(max_length=255)

    def set_tags(self, tags):
        # Serialize the array
        self.tags = ','.join(tags)

    def get_tags(self):
        # Deserialize the array
        return self.tags.split(',')

    def __str__(self):
        return self.name
