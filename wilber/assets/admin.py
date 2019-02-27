from django.contrib import admin

# Register your models here.
from .models import *

class AssetAdmin(admin.ModelAdmin):
    readonly_fields = ('image_tag',)
    list_display = ['name', 'owner']
    
class BrushAdmin(admin.ModelAdmin):
    pass
    
class PatternAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Asset, AssetAdmin)
admin.site.register(Brush)
admin.site.register(Pattern)
admin.site.register(Gradient)
admin.site.register(Plugin)
