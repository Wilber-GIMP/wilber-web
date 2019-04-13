import os

from django.db import models
from django.conf import settings
from django.core.files.storage import default_storage

from django.urls import reverse
from django.utils.safestring import mark_safe


from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver

User = settings.AUTH_USER_MODEL


def get_image_path(instance, filename):
    return os.path.join('images', str(instance.type), filename)

def get_file_path(instance, filename):
    return os.path.join('assets', str(instance.type), filename)



class AssetType(models.Model):
    name = models.CharField(max_length=32)
    folder = models.CharField(max_length=32)
    
    def __str__(self):
        return self.name
        
    def __repr__(self):
        return self.folder
    

class Asset(models.Model):
    ASSET_TYPES = [
        ('brushes', 'Brush'),
        ('patterns', 'Pattern'),
        ('gradients', 'Gradient'),
        ('plug-ins', 'Plug-in'),
    ]
    
    
    owner = models.ForeignKey(User, related_name='assets', on_delete=models.CASCADE)
    #type2 = models.CharField(max_length=9,
    #              choices=ASSET_TYPES,)
    type = models.ForeignKey('AssetType', on_delete=models.CASCADE, null=True)
                  
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    file = models.FileField(upload_to = get_file_path, null=True, blank=True)
    filesize = models.IntegerField(default=0)
    
    image = models.ImageField(upload_to = get_image_path, default = 'images/none/no-img.jpg', null=True, blank=True)
    
    num_likes = models.PositiveIntegerField(default=0)
    num_downloads = models.PositiveIntegerField(default=0)
    num_shares = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def folder(self):
        return self.type.folder
    
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




@receiver(post_save, sender=Asset)    
def update_filesize(sender, **kwargs):
    asset = kwargs["instance"]
    asset.filesize = asset.get_filesize()
    
    signals.post_save.disconnect(update_filesize, sender=Asset)
    asset.save()
    signals.post_save.connect(update_filesize, sender=Asset)
