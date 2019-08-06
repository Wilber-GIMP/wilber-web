import os

from django.db import models
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
from django.urls import reverse



from django.db.models import signals
from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver

from autoslug import AutoSlugField
from imagekit.models import ProcessedImageField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

from .validators import FileValidator, PathAndRename


from IPython import embed

User = settings.AUTH_USER_MODEL


def get_image_path(instance, filename):
    return PathAndRename('images')(instance, filename)

def get_file_path(instance, filename):
    return PathAndRename('assets')(instance, filename)




class Asset(models.Model):
    CATEGORIES = [
        ('brushes', 'Brush'),
        ('patterns', 'Pattern'),
        ('gradients', 'Gradient'),
        ('palettes', 'Palette'),
        ('plug-ins', 'Plug-in'),
    ]

    owner = models.ForeignKey(User, related_name='assets', on_delete=models.CASCADE)
    category = models.CharField(max_length=9, choices=CATEGORIES)



    name = models.CharField(max_length=100)

    slug = AutoSlugField(null=True, default=None, unique=True, populate_from='name')

    description = models.TextField(max_length=3000)
    source = models.URLField(null=True, blank=True)

    file = models.FileField(upload_to = get_file_path,
        null=True, blank=True,
        validators=[FileValidator(max_size=10*2**20)]
        )

    filesize = models.IntegerField(default=0, editable=False)


    image = ProcessedImageField(upload_to = get_image_path,
                                           default = 'images/no-img.png',
                                           null=True, blank=True,
                                           validators=[FileValidator(max_size=10*2**20)],
                                           processors=[ResizeToFit(2048, 2048)],
                                           format='JPEG',
                                           options={'quality': 80})

    image_thumbnail = ImageSpecField(source='image',
                                      processors=[ResizeToFit(300, 300)],
                                      format='JPEG',
                                      options={'quality': 60})

    likes = models.ManyToManyField(User, through='Like', related_name='liked')

    num_likes = models.PositiveIntegerField(default=0,  editable=False)
    num_downloads = models.PositiveIntegerField(default=0,  editable=False)
    num_shares = models.PositiveIntegerField(default=0,  editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def folder(self):
        return self.category

    def get_absolute_url(self):
        #return reverse('asset:detail', kwargs={'pk': self.pk})
        return reverse('asset:detail-slug', kwargs={'slug': self.slug})

    def edit_url(self):
        #return reverse('asset:edit', kwargs={'pk': self.pk})
        return reverse('asset:edit-slug', kwargs={'slug': self.slug})

    def delete_url(self):
        #return reverse('asset:delete', kwargs={'pk': self.pk})
        return reverse('asset:delete-slug', kwargs={'slug': self.slug})


    def get_filesize(self):
        if self.file and os.path.exists(self.file.path):
            return default_storage.size(self.file.path)
        return 0

    def __str__(self):
        return self.name



    def calculate_likes(self):
        return self.likes.all().count()

    def download(self):
        self.num_downloads +=1
        self.save()
        return self.num_downloads

    def is_liked(self, user):
        if user.is_anonymous:
            return False
        return Like.objects.filter(asset=self, user=user).exists()

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

    def rename_files(self, file_field, get_path):
        if file_field:
            if 'no-img.png' in os.path.basename(file_field.name):
                return
            # Create new filename, using primary key and file extension
            old_filename = file_field.name
            new_filename = get_path(self, old_filename)
            # Create new file and remove old one
            if new_filename != old_filename:
                file_field.storage.delete( new_filename )
                file_field.storage.save( new_filename, file_field )
                file_field.name = new_filename
                file_field.close()
                file_field.storage.delete(old_filename)

    def save( self, *args, **kwargs ):
        if self.pk:
            super(Asset, self ).save( *args, **kwargs)
        else:
            super(Asset, self ).save( *args, **kwargs)
            self.rename_files(self.file, get_file_path)
            self.rename_files(self.image, get_image_path)
            super(Asset, self ).save( *args, **kwargs)

class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, related_name='liked', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'asset')

    def __str__(self):
        return "%s likes %s"%(self.user.username, self.asset.name)



@receiver(post_save, sender=Asset)
def update_filesize(sender, **kwargs):
    asset = kwargs["instance"]
    asset.filesize = asset.get_filesize()

    signals.post_save.disconnect(update_filesize, sender=Asset)
    asset.save()
    signals.post_save.connect(update_filesize, sender=Asset)



def recursive_delete_path(path):
    try:
        os.rmdir(path)
    except:
        pass
    else:
        recursive_delete_path(os.path.dirname(path))

@receiver(post_delete, sender=Asset)
def submission_delete(sender, instance, **kwargs):
    filepath = instance.file.path
    instance.file.delete(False)
    recursive_delete_path(os.path.dirname(filepath))

    imagepath = instance.image.path
    instance.image.delete(False)
    recursive_delete_path(os.path.dirname(imagepath))



@receiver(post_save, sender=Like)
def do_like(sender, instance, created, **kwargs):
    if created:
        instance.asset.num_likes += 1
        instance.asset.save()

@receiver(pre_delete, sender=Like)
def unlike(sender, instance, **kwargs):
    instance.asset.num_likes -= 1
    instance.asset.save()



