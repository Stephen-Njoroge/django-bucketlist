from __future__ import unicode_literals

from django.db import models


# Create your models here.
class BaseModel(models.Model):
    name = models.CharField(blank=False, max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('modified_on',)
        abstract = True


class BucketList(BaseModel):
    owner = models.ForeignKey('auth.User', related_name='bucketlists')


class Item(BaseModel):
    is_done = models.BooleanField(default=False)
    bucketlist = models.ForeignKey(
        'BucketList',
        related_name='items', on_delete=models.CASCADE,)
