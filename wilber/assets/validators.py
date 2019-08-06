# @brief
# Performs file upload validation for django. The original version implemented
# by dokterbob had some problems with determining the correct mimetype and
# determining the size of the file uploaded (at least within my Django application
# that is).

# @author dokterbob
# @author jrosebr1

import mimetypes
import os
import time
from os.path import splitext
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat
from django.utils.deconstruct import deconstructible
from uuid import uuid4

@deconstructible
class FileValidator(object):
    """
    Validator for files, checking the size, extension and mimetype.

    Initialization parameters:
        allowed_extensions: iterable with allowed file extensions
            ie. ('txt', 'doc')
        allowd_mimetypes: iterable with allowed mimetypes
            ie. ('image/png', )
        min_size: minimum number of bytes allowed
            ie. 100
        max_size: maximum number of bytes allowed
            ie. 24*1024*1024 for 24 MB

    Usage example::

        MyModel(models.Model):
            myfile = FileField(validators=FileValidator(max_size=24*1024*1024), ...)

    """

    extension_message = _("Extension '%(extension)s' not allowed. Allowed extensions are: '%(allowed_extensions)s.'")
    mime_message = _("MIME type '%(mimetype)s' is not valid. Allowed types are: %(allowed_mimetypes)s.")
    min_size_message = _('The current file %(size)s, which is too small. The minumum file size is %(allowed_size)s.')
    max_size_message = _('The current file %(size)s, which is too large. The maximum file size is %(allowed_size)s.')

    def __init__(self, *args, **kwargs):
        self.allowed_extensions = kwargs.pop('allowed_extensions', None)
        self.allowed_mimetypes = kwargs.pop('allowed_mimetypes', None)
        self.min_size = kwargs.pop('min_size', 0)
        self.max_size = kwargs.pop('max_size', None)

    def __call__(self, value):
        """
        Check the extension, content type and file size.
        """

        # Check the extension
        ext = splitext(value.name)[1][1:].lower()
        if self.allowed_extensions and not ext in self.allowed_extensions:
            message = self.extension_message % {
                'extension' : ext,
                'allowed_extensions': ', '.join(self.allowed_extensions)
            }

            raise ValidationError(message)

        # Check the content type
        mimetype = mimetypes.guess_type(value.name)[0]
        if self.allowed_mimetypes and not mimetype in self.allowed_mimetypes:
            message = self.mime_message % {
                'mimetype': mimetype,
                'allowed_mimetypes': ', '.join(self.allowed_mimetypes)
            }

            raise ValidationError(message)

        # Check the file size
        filesize = len(value)
        if self.max_size and filesize > self.max_size:
            message = self.max_size_message % {
                'size': filesizeformat(filesize),
                'allowed_size': filesizeformat(self.max_size)
            }

            raise ValidationError(message)

        elif filesize < self.min_size:
            message = self.min_size_message % {
                'size': filesizeformat(filesize),
                'allowed_size': filesizeformat(self.min_size)
            }

            raise ValidationError(message)



@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.basepath = sub_path

    def check_if_exists(self, instance, filename):
        name = self.get_full_path(instance, filename)
        fulpath = os.path.join(settings.MEDIA_ROOT, name)

        if os.path.exists(fulpath):
            os.remove(fulpath)

    def get_path(self, instance, filename):
        timed_path = time.strftime('%Y/%m/%d')
        if instance.pk:
            return os.path.join(timed_path, instance.category, '{:0>6d}__{}'.format(instance.pk, instance.slug))
        else:
            return os.path.join(timed_path, instance.category)

    def get_filename(self, instance, filename):
        base_filename, file_ext = os.path.splitext(filename)
        if instance.pk:
            return '{:0>6d}__{}_{}{}'.format(instance.pk, instance.category, instance.slug, file_ext)
        else:
            return '{}_{}_{}{}'.format(instance.category, uuid4().hex[:6], instance.slug, file_ext)

    def get_full_path(self, instance, filename):
        path = self.get_path(instance, filename)
        new_filename = self.get_filename(instance, filename)
        return os.path.join(self.basepath, path, new_filename)


    def __call__(self, instance, filename):
        self.check_if_exists(instance, filename)
        return self.get_full_path(instance, filename)
