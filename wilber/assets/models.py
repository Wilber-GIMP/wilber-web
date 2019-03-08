from django.db import models
from django.conf import settings
from django.core.files.storage import default_storage

from django.urls import reverse
from django.utils.safestring import mark_safe

User = settings.AUTH_USER_MODEL

class Asset(models.Model):
    owner = models.ForeignKey(User, related_name='assets', on_delete=models.CASCADE)
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
        
    def save(self, *args, **kwargs):
        self.filesize = self.get_size()
        super(Asset, self).save(*args, **kwargs)
        
    def get_size(self):
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
