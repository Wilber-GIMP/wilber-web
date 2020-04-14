import logging
import os

from autoslug import AutoSlugField
from django.conf import settings
from django.core.files.base import File
from django.core.files.storage import default_storage
from django.db import models
from django.db.models import signals
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel
from imagekit.models import ImageSpecField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from .validators import FileValidator
from .validators import PathAndRename
from .wilber_package import WilberPackage

User = settings.AUTH_USER_MODEL
logger = logging.getLogger(__name__)


def get_image_path(instance, filename, remove=True):
    return PathAndRename("images", remove)(instance, filename)


def get_file_path(instance, filename, remove=True):
    return PathAndRename("assets", remove)(instance, filename)


class Asset(TimeStampedModel, models.Model):
    CATEGORIES = [
        ("brushes", "Brush"),
        ("patterns", "Pattern"),
        ("gradients", "Gradient"),
        ("palettes", "Palette"),
        ("plug-ins", "Plug-in"),
    ]

    owner = models.ForeignKey(
        User, related_name="assets", on_delete=models.CASCADE
    )
    category = models.CharField(max_length=9, choices=CATEGORIES)

    name = models.CharField(max_length=100)

    slug = AutoSlugField(
        null=True, default=None, unique=True, populate_from="name"
    )

    description = models.TextField(max_length=3000)
    source = models.URLField(null=True, blank=True)

    file = models.FileField(
        max_length=255,
        upload_to=get_file_path,
        null=True,
        blank=True,
        validators=[FileValidator(max_size=10 * 2 ** 20)],
    )

    filesize = models.IntegerField(default=0, editable=False)

    image = ProcessedImageField(
        max_length=255,
        upload_to=get_image_path,
        default="images/no-img.png",
        null=True,
        blank=True,
        validators=[FileValidator(max_size=10 * 2 ** 20)],
        processors=[ResizeToFit(2048, 2048)],
        format="JPEG",
        options={"quality": 80},
    )

    image_thumbnail = ImageSpecField(
        source="image",
        processors=[ResizeToFit(300, 300)],
        format="JPEG",
        options={"quality": 60},
    )

    likes = models.ManyToManyField(User, through="Like", related_name="liked")

    num_likes = models.PositiveIntegerField(default=0, editable=False)
    num_downloads = models.PositiveIntegerField(default=0, editable=False)
    num_views = models.PositiveIntegerField(default=0, editable=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def folder(self):
        return self.category

    def get_absolute_url(self):
        # return reverse('asset:detail', kwargs={'pk': self.pk})
        return reverse("asset:detail-slug", kwargs={"slug": self.slug})

    def url(self):
        return self.get_absolute_url()

    def edit_url(self):
        # return reverse('asset:edit', kwargs={'pk': self.pk})
        return reverse("asset:edit-slug", kwargs={"slug": self.slug})

    def delete_url(self):
        # return reverse('asset:delete', kwargs={'pk': self.pk})
        return reverse("asset:delete-slug", kwargs={"slug": self.slug})

    def get_filesize(self):
        if self.file and os.path.exists(self.file.path):
            return default_storage.size(self.file.path)
        return 0

    def __str__(self):
        return self.name

    def calculate_likes(self):
        return self.likes.all().count()

    def download(self):
        self.num_downloads += 1
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

    def toggle_like(self, user):
        like, created = self.do_like(user)
        if not created:
            self.unlike(user)
            return False
        else:
            return True

    def delete(self, using=None, keep_parents=False):
        print("METHOD DELETE")
        return super(Asset, self).delete(using, keep_parents)

    def save(self, **kwargs):
        print("SAVE METHOD")
        return super(Asset, self).save(**kwargs)


class Like(models.Model):
    user = models.ForeignKey(
        User, related_name="likes", on_delete=models.CASCADE
    )
    asset = models.ForeignKey(
        Asset, related_name="liked", on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "asset")

    def __str__(self):
        return "%s likes %s" % (self.user.username, self.asset.name)


def update_filesize(asset):
    asset.filesize = asset.get_filesize()


def rename_file(asset, file_field, get_path):
    if file_field:
        if "no-img.png" in os.path.basename(file_field.name):
            return
        # Create new filename, using primary key and file extension
        old_filename = file_field.name
        new_filename = get_path(asset, old_filename, False)
        # Create new file and remove old one
        logger.info("RENAME FROM %s TO %s", old_filename, new_filename)
        if new_filename != old_filename:
            file_field.storage.delete(new_filename)
            file_field.storage.save(new_filename, file_field)
            file_field.name = new_filename
            file_field.close()
            file_field.storage.delete(old_filename)


# @receiver(post_save, sender=Asset)
def rename_files(asset):
    print("RENAMING: ")
    rename_file(asset, asset.file, get_file_path)
    rename_file(asset, asset.image, get_image_path)


def process_package(file_field, pk, slug):
    wilber_package = WilberPackage(file_field.path)
    new_package, message = wilber_package.process(pk, slug)
    print(message)
    if new_package:
        file_field.save(file_field.name, File(open(new_package, "rb")))
    wilber_package.clean()


@receiver(post_save, sender=Asset)
def post_save_asset(sender, **kwargs):
    signals.post_save.disconnect(post_save_asset, sender=Asset)
    asset = kwargs["instance"]

    rename_files(asset)
    asset.save()
    if asset.file:
        process_package(asset.file, asset.pk, asset.slug)

    update_filesize(asset)
    asset.save()
    signals.post_save.connect(post_save_asset, sender=Asset)


def recursive_delete_path(path):
    print("RECURSIVE DELETE:", path)
    try:
        os.rmdir(path)
    except os.error:
        pass
    else:
        recursive_delete_path(os.path.dirname(path))


@receiver(post_save, sender=Like)
def do_like(sender, instance, created, **kwargs):
    if created:
        instance.asset.num_likes += 1
        instance.asset.save()


@receiver(pre_delete, sender=Like)
def unlike(sender, instance, **kwargs):
    instance.asset.num_likes -= 1
    instance.asset.save()


def _delete_file(path):
    # Deletes file from filesystem.
    print("DELTEEEEEEETE", path)
    if os.path.isfile(path):
        os.remove(path)

        recursive_delete_path(os.path.dirname(path))


@receiver(pre_delete, sender=Asset)
def delete_img_pre_delete_asset(sender, instance, *args, **kwargs):
    print("SIGNAL pre delete")
    # return
    if instance.file:
        instance.file.delete(False)
        recursive_delete_path(os.path.dirname(instance.file.path))

    if instance.image and "no-img" not in instance.image.name:
        instance.image.delete(False)
        recursive_delete_path(os.path.dirname(instance.image.path))


@receiver(post_delete, sender=Asset)
def delete_img_post_delete_asset(sender, instance, **kwargs):
    print("SIGNAL post delete")
    return
    if instance.file:
        filepath = instance.file.path
        instance.file.delete(False)
        recursive_delete_path(os.path.dirname(filepath))
    if instance.image:
        imagepath = instance.image.path
        if "no-img.png" not in imagepath:
            instance.image.delete(False)
            recursive_delete_path(os.path.dirname(imagepath))
