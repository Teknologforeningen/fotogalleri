from django.db import models
from json import dumps, loads
from os.path import join


def new_image_path(instance, filename):
    return filename


class ImageMetadata(models.Model):
    '''
    Metadata model for uploaded images.

    Stores simple metadata such as file name, path, and time and date of upload.
    '''
    filename = models.CharField(max_length=256)
    image = models.ImageField(upload_to=new_image_path)
    upload_time = models.DateTimeField(auto_now_add=True, blank=True)
    # JSON array formatted as a string for containing all thumbnails
    thumbnails_json = models.CharField(max_length=256, blank=True, null=True, default='[]')

    def set_thumbnails(self, new_thumbnails):
        thumbnails = self.thumbnails + list(new_thumbnails)
        # Setting separators will give the most compact JSON representation
        thumbnails_json = dumps(thumbnails, separators=(',', ':'))
        self.thumbnails_json = thumbnails_json
        self.save()

    def _get_thumbnails(self):
        return loads(self.thumbnails_json)

    thumbnails = property(_get_thumbnails)

    def _get_subfolder(self):
        subfolder = str(self.pk // 1000)
        return '{}000'.format(subfolder)

    def save(self, *args, **kwargs):
        is_saved = self.pk is not None
        super(ImageMetadata, self).save(*args, **kwargs)

        if not is_saved and self.image:
            oldfile = self.image.name
            subfolder = self._get_subfolder()
            newfile = join(subfolder, oldfile)

            self.image.storage.save(newfile, self.image)
            self.image.name = newfile
            self.image.close()
            self.image.storage.delete(oldfile)

    def __str__(self):
        return '{name};{path};{time}'.format(name=self.filename,
                                             path=self.image,
                                             time=self.upload_time)
