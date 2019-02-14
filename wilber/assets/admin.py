from django.contrib import admin

# Register your models here.
from .models import Asset, Brush, Pattern

class AssetAdmin(admin.ModelAdmin):
    pass
    
class BrushAdmin(admin.ModelAdmin):
    pass
    
class PatternAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Asset, AssetAdmin)
admin.site.register(Brush, BrushAdmin)
admin.site.register(Pattern, PatternAdmin)
