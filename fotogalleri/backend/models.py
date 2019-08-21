from django.db import models
from os import path


def new_image_path(instance, filename):
    '''
    Image will be uploaded to MEDIA_ROOT/<input_dirs>/<filename>
    '''
    return path.join(instance.input_dirs, filename)


class ImageMetadata(models.Model):
    '''
    Metadata model for uploaded images.

    Stores simple metadata such as file name, path, and time and date of upload.
    '''
    filename = models.CharField(max_length=255)
    image_path = models.ImageField(upload_to=new_image_path)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __init__(self, input_dirs, img_width_field=None, img_height_field=None, *args, **kwargs):
        self.input_dirs = input_dirs
        self.width_field = img_width_field
        self.height_field = img_height_field
        super(ImageMetadata, self).__init__(*args, **kwargs)

    def _get_width(self):
        width = self.width_field
        if not width:
            try:
                width = self.image_path.width_field
            except Exception:
                raise ValueError(
                        'Save ImageMetadata object for getting width. Alternatively provide <img_width_field>')
        return width

    def _get_height(self):
        height = self.height_field
        if not height:
            try:
                height = self.image_path.height_field
            except Exception:
                raise ValueError(
                        'Save ImageMetadata object for getting height. Alternatively provide <img_height_field>')
        return height

    width = property(_get_width)
    height = property(_get_height)

    def __str__(self):
        return '{name};{path};{w}x{h};{time}'.format(name=self.filename,
                                                     path=self.image_path,
                                                     w=self.width,
                                                     h=self.height,
                                                     time=self.created_at)
