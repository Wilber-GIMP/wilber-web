from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db.transaction import atomic
from os.path import basename
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

    def image_tag(self, obj):
        if obj.image:
            name = basename(obj.image.name)
            return mark_safe('<img src="%s"  height="300" />' % (obj.image.url))
        return "No Image"
    image_tag.short_description = 'Image'

    def image_link(self, obj):
        if obj.image:
            name = basename(obj.image.name)
            return mark_safe('<a href="%s">%s</a>' % (obj.image.url, name))
    image_link.short_description = 'Image'

    def file_link(self, obj):
        if obj.file:
            name = basename(obj.file.name)
            return mark_safe('<a href="%s">%s</a>' % (obj.file.url, name))
    file_link.short_description = 'File'

    readonly_fields = ('image_tag', 'slug', 'created', 'modified')
    list_display = ['name', 'category', 'owner',   'image_link', 'file_link', 'slug', 'get_filesize', 'num_likes',]
    search_fields = ['name', 'owner__username']
    list_filter = ['category',]
    actions = [recalculate_likes]





class LikeAdmin(admin.ModelAdmin):
    list_display = ['asset', 'user', 'timestamp']
    search_fields = ['asset', 'user']



admin.site.register(Asset, AssetAdmin)
#admin.site.register(AssetType)
admin.site.register(Like, LikeAdmin)
