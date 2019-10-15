from django.db import models
from json import dumps, loads
from os.path import join


def new_image_path(instance, filename):
    return filename


class ImageMetadata(models.Model):
    '''
    Metadata model for uploaded images.
    Stores simple metadata such as file name, path, and time and date of upload.

    Images are stored in the following manner /<year>/<event_name>/<image_name>
    '''
    year = models.CharField(max_length=256, blank=False, null=False)
    event = models.CharField(max_length=256, blank=False, null=False)
    image = models.ImageField(upload_to=new_image_path)
    upload_time = models.DateTimeField(auto_now_add=True, blank=True)
    # JSON array formatted as a string for containing all thumbnails
    thumbnails_json = models.CharField(max_length=256, blank=False, null=False, default='[]')

    def set_thumbnails(self, new_thumbnails):
        thumbnails = self.thumbnails + list(new_thumbnails)
        # Setting separators will give the most compact JSON representation
        thumbnails_json = dumps(thumbnails, separators=(',', ':'))
        self.thumbnails_json = thumbnails_json
        self.save()

    def _get_thumbnails(self):
        return loads(self.thumbnails_json)

    thumbnails = property(_get_thumbnails)

    def save(self, *args, **kwargs):
        is_saved = self.pk is not None
        super(ImageMetadata, self).save(*args, **kwargs)

        if not is_saved and self.image:
            oldfile = self.image.name
            newfile = join(self.year, self.event, oldfile)

            self.image.storage.save(newfile, self.image)
            self.image.name = newfile
            self.image.close()
            self.image.storage.delete(oldfile)

    def __str__(self):
        return '{path};{time}'.format(path=self.image,
                                      time=self.upload_time)
