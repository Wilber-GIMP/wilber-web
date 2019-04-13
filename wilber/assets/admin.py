from django.contrib import admin
from django.utils.html import format_html
# Register your models here.
from .models import *

from .admin_utils import field


def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


class AssetAdmin(admin.ModelAdmin):
    
    @field('filesize', 'filesize')
    def get_filesize(self, obj):
        return sizeof_fmt(obj.filesize)
    
    readonly_fields = ('image_tag',)
    list_display = ['name',   'owner', 'get_filesize']
    search_fields = ['name']
    #list_filter = ['type',]
    
    
admin.site.register(Asset, AssetAdmin)
admin.site.register(AssetType)
