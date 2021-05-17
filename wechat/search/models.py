from django.db import models

# Create your models here.

class Links(models.Model):
    title = models.CharField(max_length=100)#分类名
    urls = models.CharField(max_length=1024)#分类名
    image = models.CharField(max_length=1024)#分类名
