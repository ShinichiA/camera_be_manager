from django.db import models
from ..dvr_infos.models import DvrInfo


class ChannelInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    dvr = models.ForeignKey(DvrInfo, on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=50, blank=False)
    channel_no = models.IntegerField(blank=False)
    status = models.IntegerField(blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

    class Meta:
        unique_together = ["dvr", "channel_no"]
        ordering = ['id']
        db_table = 'channel_infos'
