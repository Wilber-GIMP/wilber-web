from django.db import models
from django.conf import settings
from django.core.files.storage import default_storage

from django.urls import reverse
from django.utils.safestring import mark_safe


from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver

User = settings.AUTH_USER_MODEL

class Asset(models.Model):
    ASSET_TYPES = [
        ('brush', 'Brush'),
        ('pattern', 'Pattern'),
        ('gradient', 'Gradient'),
        ('plugin', 'Plugin'),
    ]
    
    
    owner = models.ForeignKey(User, related_name='assets', on_delete=models.CASCADE)
    type = models.CharField(max_length=9,
                  choices=ASSET_TYPES,)
                  
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)

    file = models.FileField(upload_to = 'assets/', null=True, blank=True)
    filesize = models.IntegerField(default=0)
    
    image = models.ImageField(upload_to = 'images/', default = 'images/none/no-img.jpg', null=True, blank=True)
    thumbnail = models.ImageField(upload_to = 'thumbnails/', default = 'images/none/no-thumb.jpg', null=True, blank=True)
    
    num_likes = models.PositiveIntegerField(default=0)
    num_downloads = models.PositiveIntegerField(default=0)
    num_shares = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_absolute_url(self):
        return reverse('asset:detail', kwargs={'pk': self.pk})
        
        
    def get_filesize(self):
        if self.file:
            return default_storage.size(self.file.path)
        return 0
    
    def __str__(self):
        return self.name
        
    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="150" height="150" />' % (self.image))

    image_tag.short_description = 'Image'
    
    def add_like(self):
        self.num_likes += 1
        self.save()


class Brush(Asset):
    pass

class Pattern(Asset):
    pass

class Gradient(Asset):
    pass

class Plugin(Asset):
    pass




@receiver(post_save, sender=Asset)    
def update_filesize(sender, **kwargs):
    asset = kwargs["instance"]
    asset.filesize = asset.get_filesize()
    
    signals.post_save.disconnect(update_filesize, sender=Asset)
    asset.save()
    signals.post_save.connect(update_filesize, sender=Asset)
