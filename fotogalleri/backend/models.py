from django.db.models import Model, CharField, ImageField, DateTimeField, ForeignKey, CASCADE
from json import dumps, loads
from os.path import join


def new_image_path(instance, filename):
    return filename


class ImageMetadata(Model):
    '''
    Metadata model for uploaded images.
    Stores simple metadata such as file name, path, and time and date of upload.
    '''
    # FIXME: refactor on_delete
    path = ForeignKey('ImagePath', on_delete=CASCADE, blank=True, null=True)
    image = ImageField(upload_to=new_image_path)
    upload_time = DateTimeField(auto_now_add=True, blank=True)
    # JSON array formatted as a string for containing all thumbnails
    thumbnails_json = CharField(max_length=256, blank=False, null=False, default='[]')

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
            newfile = join(self.path.full_path if self.path else '', self.image.name)
            if newfile != oldfile:
                self.image.storage.save(newfile, self.image)
                self.image.name = newfile
                self.image.close()
                self.image.storage.delete(oldfile)

    def __str__(self):
        return '{path};{time}'.format(path=self.image, time=self.upload_time)


class ImagePath(Model):
    # FIXME: refactor on_delete
    parent = ForeignKey('self', on_delete=CASCADE, blank=True, null=True)
    path = CharField(max_length=256, blank=False, null=False, unique=True)

    def _get_full_path(self):
        return join(self.parent.full_path if self.parent else '', self.path)

    full_path = property(_get_full_path)

    def _is_root_child(self):
        '''
        Returns true if this ImagePath is a first descendant of the root (i.e. empty parent).
        '''
        return not self.parent

    is_root_child = property(_is_root_child)

    def __str__(self):
        return self.full_path

    @staticmethod
    def create(path, parent):
        new_image_path = ImagePath(path=path, parent=parent)
        new_image_path.save()
        return new_image_path
