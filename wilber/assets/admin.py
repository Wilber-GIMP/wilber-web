from django.contrib import admin
from django.utils.html import format_html

from django.db.transaction import atomic
# Register your models here.
from .models import *

from .admin_utils import field


def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


@atomic
def recalculate_likes(modeladmin, request, queryset):
    for asset in queryset:
        asset.num_likes = asset.calculate_likes()
        asset.save()
recalculate_likes.short_description = "Recalculate number of likes of each asset"



class AssetAdmin(admin.ModelAdmin):

    @field('filesize', 'filesize')
    def get_filesize(self, obj):
        return sizeof_fmt(obj.filesize)

    readonly_fields = ('image_tag',)
    list_display = ['name', 'category', 'owner', 'get_filesize', 'num_likes', 'image', 'slug']
    search_fields = ['name']
    #list_filter = ['type',]
    actions = [recalculate_likes]





class LikeAdmin(admin.ModelAdmin):
    list_display = ['asset', 'user', 'timestamp']
    search_fields = ['asset', 'user']



admin.site.register(Asset, AssetAdmin)
#admin.site.register(AssetType)
admin.site.register(Like, LikeAdmin)
