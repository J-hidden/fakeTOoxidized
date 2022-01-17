from django.db import models

# Create your models here.


class Oxidized(models.Model):
    name = models.CharField(verbose_name='设备名', max_length=128)
    ip = models.GenericIPAddressField(verbose_name='IP地址', max_length=128)
    platform = models.CharField(verbose_name='设备类型', max_length=128)
    group = models.CharField(verbose_name='所属组', max_length=128)
    state = models.BooleanField(verbose_name='最后一次采集的状态', default=False, max_length=128)
    last_update = models.DateTimeField(verbose_name='最后一次更新的时间', max_length=128, auto_now=True)
    last_change = models.DateTimeField(verbose_name='最后一次更改的时间', max_length=128)
    config = models.TextField(verbose_name='配置信息', max_length=128)
    diff = models.TextField(verbose_name='差异信息', max_length=128, default='null')


class Device(models.Model):
    name = models.CharField(verbose_name='设备名', max_length=128)
    ip = models.GenericIPAddressField(verbose_name='IP地址', max_length=128)
    platform = models.CharField(verbose_name='设备类型', max_length=128)
    group = models.CharField(verbose_name='所属组', max_length=128)
    username = models.CharField(verbose_name='用户名', max_length=128)
    password = models.CharField(verbose_name='密码', max_length=128)
    port = models.CharField(verbose_name='端口号', default=22, max_length=128)



