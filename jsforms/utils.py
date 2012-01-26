from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files import File
import os
from cStringIO import StringIO
import datetime

JSFORMS_THUMBNAIL_SIZE = getattr(settings, 'JSFORMS_THUMBNAIL_SIZE', (45,45))


# imports PIL with error handling
try:
    import Image as PIL
except ImportError:
    PIL = None
    try:
        if settings.JSFORMS_IMAGEUPLOAD_FEATURE:
            raise Exception("jsforms did not find PIL. Either turn off the Image Upload Feature or install PIL.")
    except AttributeError: pass


def upload_to(instance, fullpath):
    dirname, filename = os.path.split(fullpath)
    if s3:
        path = os.path.join(
            'jswidgets/temporary_images',
            str(int(datetime.datetime.now().strftime("%s"))),
            filename
            )
    else:
        # TODO: we should implement this
        return 'we seem to not have implemented this feature'
    print "uploading to %s" % path
    return path



def fs_thumbnail_generator(image=None, name=None):
    orig_path = os.path.join(settings.MEDIA_ROOT, image.path)

    dir, file = os.path.split(orig_path)
    thumb_path = os.path.join(settings.MEDIA_ROOT, "temporary_thumbs", file)

    # Create thumbnail
    thumb = PIL.open(orig_path)
    thumb.thumbnail(JSFORMS_THUMBNAIL_SIZE)
    thumb.save(thumb_path, "JPEG", quality=80)

    _, file = os.path.split(image.url)
    return os.path.join(settings.MEDIA_URL, "temporary_thumbs", file)


def s3_thumbnail_generator(image=None, name=None):
    thumb_filename = "jswidgets/thumbs/%s" % image.name
    try:
        aws_file = default_storage.open(thumb_filename)
        print "I found a thumbnail", thumb_filename
    except IOError:
        thumb = PIL.open(image.file)
        thumb.thumbnail(JSFORMS_THUMBNAIL_SIZE)
        filelikeobj = StringIO()
        thumb.save(filelikeobj, 'JPEG', quality=80)
        filelikeobj.seek(0)
        default_storage.save(thumb_filename, File(filelikeobj))
        aws_file = default_storage.open(thumb_filename)
        print "I built a thumbnail", thumb_filename
    return default_storage.url(aws_file.name)

def get_or_create_thumbnail(*args, **kwargs): return ''
s3 = False
if PIL:
    storage = getattr(settings, 'DEFAULT_FILE_STORAGE', 'fs')
    if 's3' in storage.lower():
        s3 = True
        get_or_create_thumbnail = s3_thumbnail_generator
    else:
        get_or_create_thumbnail = fs_thumbnail_generator



