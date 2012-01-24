from django.db import models
from django.conf import settings
from os import path

try:
    import Image as PIL
except ImportError:
    PIL = None
    try:
        if settings.JSWIDGET_IMAGEUPLOAD_FEATURE:
            raise Exception("jsforms did not find PIL. Either turn off the Image Upload Feature or install PIL.")
    except AttributeError: pass

try:
    JSWIDGET_THUMBNAIL_SIZE = settings.JSWIDGET_THUMBNAIL_SIZE
except AttributeError:
    JSWIDGET_THUMBNAIL_SIZE = (45,45)


class TemporaryUploadedImage(models.Model):
    timage = models.ImageField(max_length=500, upload_to="temporary_images")

    def create_thumbnails(self, force=False):
        ''' Use PIC_THUMBNAILS to determine which thumbnails to create '''
        orig_path = path.join(settings.MEDIA_ROOT, self.timage.path)

        thumb_path = self.get_thumb_path(orig_path)

        # Create thumbnail
        thumb = PIL.open(orig_path)
        thumb.thumbnail(JSWIDGET_THUMBNAIL_SIZE)
        thumb.save(thumb_path, "JPEG", quality=80)

    def get_thumb_url(self):
        dir, file = path.split(self.timage.url)
        return path.join(dir, "..", "temporary_thumbs", file)

    def get_thumb_path(self, orig_path):
        dir, file = path.split(orig_path)
        return path.join(dir, "..", "temporary_thumbs", file)

    def save(self, *args, **kwargs):
        super(TemporaryUploadedImage, self).save(*args, **kwargs)
        if PIL:
            self.create_thumbnails()
