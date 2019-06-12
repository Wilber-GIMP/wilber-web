import os

from django.db import models
from django.conf import settings
from django.core.files.storage import default_storage

from django.urls import reverse
from django.utils.safestring import mark_safe


from django.db.models import signals
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

User = settings.AUTH_USER_MODEL


def get_image_path(instance, filename):
    return os.path.join('images', str(instance.type), filename)

def get_file_path(instance, filename):
    return os.path.join('assets', str(instance.type), filename)




    

class Asset(models.Model):
    CATEGORIES = [
        ('brushes', 'Brush'),
        ('patterns', 'Pattern'),
        ('gradients', 'Gradient'),
        ('plug-ins', 'Plug-in'),
    ]
    
    
    owner = models.ForeignKey(User, related_name='assets', on_delete=models.CASCADE)
    category = models.CharField(max_length=9, choices=CATEGORIES)
    #type = models.ForeignKey('AssetType', on_delete=models.CASCADE, null=True)
                  
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    file = models.FileField(upload_to = get_file_path, null=True, blank=True)
    filesize = models.IntegerField(default=0)
    
    image = models.ImageField(upload_to = get_image_path, default = 'images/none/no-img.jpg', null=True, blank=True)
    likes = models.ManyToManyField(User, through='Like', related_name='liked')
    
    num_likes = models.PositiveIntegerField(default=0)
    num_downloads = models.PositiveIntegerField(default=0)
    num_shares = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def folder(self):
        return self.category
    
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
    
    def calculate_likes(self):
        return self.likes.all().count()
        
    def download(self):
        self.num_downloads +=1
        self.save()
        return self.num_downloads
    
    def do_like(self, user):
        like, created = Like.objects.get_or_create(user=user, asset=self)
        return like, created
    
    def unlike(self, user):
        try:
            like = Like.objects.get(user=user, asset=self)
            like.delete()
            return True
        except Like.DoesNotExist:
            return False

class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, related_name='liked', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'asset')
    
    def __str__(self):
        return f'{self.user.username} likes \'{self.asset.name}\''
        


@receiver(post_save, sender=Asset)    
def update_filesize(sender, **kwargs):
    asset = kwargs["instance"]
    asset.filesize = asset.get_filesize()
    
    signals.post_save.disconnect(update_filesize, sender=Asset)
    asset.save()
    signals.post_save.connect(update_filesize, sender=Asset)



@receiver(post_save, sender=Like)
def do_like(sender, instance, created, **kwargs):
    if created:
        instance.asset.num_likes += 1
        instance.asset.save()
    
@receiver(pre_delete, sender=Like)
def unlike(sender, instance, **kwargs):
    instance.asset.num_likes -= 1
    instance.asset.save()
