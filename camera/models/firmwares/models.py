from django.db import models


class FirmwareInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    version = models.CharField(max_length=50, blank=False)
    firmware = models.IntegerField(blank=False)
    description = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id

    class Meta:
        ordering = ['id']
        db_table = 'firmwares'
