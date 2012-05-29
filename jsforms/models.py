from django.db import models
from . import utils


class TemporaryUploadedImage(models.Model):
    timage = models.ImageField(max_length=500, upload_to=utils.upload_to)

    def get_thumb_url(self):
        try:
            return self._thumburls['thumbnail']
        except AttributeError:
            self._thumburls = utils.get_or_create_thumbnail(image=self.timage)
            return self._thumburls['thumbnail']

    @property
    def all_othersize_urls(self):
        try:
            return self._thumburls
        except AttributeError:
            self._thumburls = utils.get_or_create_thumbnail(image=self.timage)
            return self._thumburls


    def save(self, *args, **kwargs):
        super(TemporaryUploadedImage, self).save(*args, **kwargs)
        utils.get_or_create_thumbnail(image=self.timage)
