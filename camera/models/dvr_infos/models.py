from django.db import models


class DvrInfo(models.Model):
    CONNECT_TYPE = (
        (0, 'local'),
        (1, 'public')
    )

    dvr_name = models.CharField(max_length=50, blank=False, unique=True)
    sn = models.CharField(max_length=20, unique=True)
    device_type = models.CharField(max_length=50)
    dvr_no = models.IntegerField(blank=False)
    s_no = models.IntegerField(blank=False)
    local_ip = models.GenericIPAddressField()
    local_port_http = models.IntegerField()
    local_port_tcp = models.IntegerField()
    public_ip = models.GenericIPAddressField()
    public_port_http = models.IntegerField()
    public_port_tcp = models.IntegerField()
    connect_type = models.IntegerField(choices=CONNECT_TYPE, blank=False)
    username = models.CharField(max_length=20, blank=False)
    password = models.CharField(max_length=20, blank=False)
    status = models.IntegerField(blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.dvr_name

    class Meta:
        ordering = ['id']
        db_table = 'dvr_infos'
