from django.contrib import admin
from oxidized.models import Oxidized, Device
# Register your models here.


@admin.register(Oxidized)
class OxidizedAdmin(admin.ModelAdmin):
    list_display = ['name', 'ip', 'platform', 'group', 'state', 'last_update', 'last_change', 'diff']


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'ip', 'platform', 'username', 'password', 'port', 'group']