from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files import File
import os
from cStringIO import StringIO
import datetime

JSFORMS_THUMBNAIL_SIZE = getattr(settings, 'JSFORMS_THUMBNAIL_SIZE')

if JSFORMS_THUMBNAIL_SIZE is None:
    JSFORMS_THUMBNAIL_SIZE = { 'thunbnail': (45,45) }

# for compatibility with previous settings spec.
if isinstance(JSFORMS_THUMBNAIL_SIZE, tuple):
    JSFORMS_THUMBNAIL_SIZE = { 'thumbnail' : JSFORMS_THUMBNAIL_SIZE }

def PIL_1():
    import Image as PIL
    PIL.open
    return PIL

def PIL_2():
    import PIL
    PIL.open
    return PIL

def PIL_3():
    from PIL import Image as PIL
    PIL.open
    return PIL

PIL = None
for pil_getter in [PIL_1, PIL_2, PIL_3]:
    error = False
    try:
        PIL = pil_getter()
    except ImportError: error = True
    except AttributeError: error = True
    if not error and PIL:
        break
    PIL = None

if not PIL:
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
    img = PIL.open(orig_path)
    return_dict = {}
    
    for name, size in JSFORMS_THUMBNAIL_SIZE.items():

        thumb_path = os.path.join(settings.MEDIA_ROOT, "temporary_"+name, file)

        # Create thumbnail
        thumb = img.copy()
        thumb.thumbnail(size)
        thumb.save(thumb_path, "JPEG", quality=80)

        _, file = os.path.split(image.url)
        return_dict[name] = os.path.join(settings.MEDIA_URL, "temporary_"+name, file)
    return return_dict


def s3_thumbnail_generator(image=None, name=None):
    img = None
    return_dict = {}
    for sizename, size in JSFORMS_THUMBNAIL_SIZE.items():
        thumb_filename = "jswidgets/%s/%s" % (sizename,  image.name)
        try:
            aws_file = default_storage.open(thumb_filename)
            print "I found a thumbnail", thumb_filename
        except IOError:
            if img is None:
                img = PIL.open(image.file)
            thumb = img.copy()
            thumb.thumbnail(size)
            filelikeobj = StringIO()
            thumb.save(filelikeobj, 'JPEG', quality=80)
            filelikeobj.seek(0)
            thumb_filename = "jswidgets/%s/%s" % (sizename, image.name)
            default_storage.save(thumb_filename, File(filelikeobj))
            aws_file = default_storage.open(thumb_filename)
            print "I built a thumbnail", thumb_filename
        return_dict[sizename] = default_storage.url(aws_file.name)

    return return_dict

def get_or_create_thumbnail(*args, **kwargs): return ''
s3 = False
if PIL:
    storage = getattr(settings, 'DEFAULT_FILE_STORAGE', 'fs')
    if 's3' in storage.lower():
        s3 = True
        get_or_create_thumbnail = s3_thumbnail_generator
    else:
        get_or_create_thumbnail = fs_thumbnail_generator



