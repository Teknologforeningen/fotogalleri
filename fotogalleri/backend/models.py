from django.db import models
from os import path
import json


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
    filename = models.CharField(max_length=256)
    image_path = models.ImageField(upload_to=new_image_path)
    upload_time = models.DateTimeField(auto_now_add=True, blank=True)
    # JSON array formatted as a string for containing all thumbnails
    thumbnails_json = models.CharField(max_length=256, blank=True, null=True, default=None)

    def __init__(self, input_dirs, img_width_field=None, img_height_field=None, *args, **kwargs):
        self.input_dirs = input_dirs
        self.width_field = img_width_field
        self.height_field = img_height_field
        super(ImageMetadata, self).__init__(*args, **kwargs)

    def _get_dimension(self, dimension):
        attribute = '{}_field'.format(dimension)
        dimension = getattr(self, attribute)
        if not dimension:
            try:
                dimension = getattr(self.image_path, attribute)
            except Exception:
                raise ValueError(
                    'Save ImageMetadata object for getting {dimension}. '
                    'Alternatively provide <img_{attribute}>'.format(dimension=dimension,
                                                                     attribute=attribute))
        return dimension

    def _get_width(self):
        return self._get_dimension('width')

    def _get_height(self):
        return self._get_dimension('height')

    width = property(_get_width)
    height = property(_get_height)

    def set_thumbnails(self, new_thumbnails):
        thumbnails = self.thumbnails + list(new_thumbnails)
        # Setting separators will give the most compact JSON representation
        thumbnails_json = json.dumps(thumbnails, separators=(',', ':'))
        self.thumbnails_json = thumbnails_json
        self.save()

    def _get_thumbnails(self):
        return json.loads(self.thumbnails_json)

    thumbnails = property(_get_thumbnails)

    def __str__(self):
        return '{name};{path};{w}x{h};{time}'.format(name=self.filename,
                                                     path=self.image_path,
                                                     w=self.width,
                                                     h=self.height,
                                                     time=self.created_at)
