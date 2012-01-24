from django.conf import settings
from os import path

from .models import PIL, JSFORMS_THUMBNAIL_SIZE


def image_to_thumb_url(image=None, name=None):
    orig_path = path.join(settings.MEDIA_ROOT, image.path)

    dir, file = path.split(orig_path)
    thumb_path = path.join(dir, "..", "temporary_thumbs", file)

    # Create thumbnail
    thumb = PIL.open(orig_path)
    thumb.thumbnail(JSFORMS_THUMBNAIL_SIZE)
    print "PATH %s" % thumb_path
    thumb.save(thumb_path, "JPEG", quality=80)

    dir, file = path.split(image.url)
    return path.join(dir, "..", "temporary_thumbs", file)

