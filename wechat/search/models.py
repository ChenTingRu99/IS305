# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser


class Accounts(models.Model):
    public_name = models.CharField(max_length=255)
    wechat_id = models.CharField(primary_key=True, max_length=255)
    public_image = models.CharField(max_length=255)
    authentication = models.CharField(max_length=255, blank=True, null=True)
    introduction = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'accounts'


class Articles(models.Model):
    account = models.CharField(max_length=255)
    title = models.CharField(primary_key=True, max_length=255)
    url = models.CharField(max_length=2083)
    images = models.CharField(max_length=255)
    abstract = models.CharField(max_length=255, blank=True, null=True)
    publish_date = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = '上海交通大学'


class Base(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def setDb_table(Class, tableName):
        class Meta:
            db_table = tableName

        attrs = {
            '__module__': Class.__module__,
            'Meta': Meta
        }
        return type(tableName, (Class,), attrs)


def table_model_factory(table_name):
    class TableModel(models.Model):
        # user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
        # major = models.TextField(default='', blank=True)
        account = models.CharField(max_length=255)
        title = models.CharField(primary_key=True, max_length=255)
        url = models.CharField(max_length=2083)
        images = models.CharField(max_length=255)
        abstract = models.CharField(max_length=255, blank=True, null=True)
        publish_date = models.CharField(max_length=255)

        class Meta:
            db_table = table_name
            managed = False
            ordering = ('publish_date','title')
    return TableModel




