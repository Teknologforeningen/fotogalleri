from django.db.models import Model, CASCADE
from django.db.models import CharField, ImageField, DateTimeField
from django.db.models import ForeignKey, OneToOneField
from django.conf import settings
from json import dumps, loads
from os.path import join, splitext, normpath
from os import sep
from backend.thumbnail.thumbnail_utils import create_thumbnail_name


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

    def _find_preview_thumbnail(self):
        thumbnails = self._get_thumbnails()
        for thumbnail in thumbnails:
            w, h = thumbnail
            if 300 - 5 <= w <= 300 + 5:
                return thumbnail
            if 300 - 5 <= h <= 300 + 5:
                return thumbnail
        return None

    def _get_preview_thumbnail(self):
        thumbnail = self._find_preview_thumbnail()
        if thumbnail is None:
            return self.image.url

        raw_filepath, _ = splitext(self.image.name)
        raw_filename = normpath(raw_filepath).split(sep)[-1]
        thumbnail_filename = create_thumbnail_name(raw_filename, *thumbnail)
        return join(settings.MEDIA_URL, self.path.path, settings.THUMBNAILS_NAME, thumbnail_filename)

    preview = property(_get_preview_thumbnail)

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
                self.save()

            if not self.path:
                root_image, created = RootImage.objects.get_or_create(image_metadata=self)
                if created:
                    root_image.save()

    def __str__(self):
        return '{path};{time}'.format(path=self.image, time=self.upload_time)


class RootImage(Model):
    image_metadata = OneToOneField(ImageMetadata, on_delete=CASCADE, primary_key=True)


class ImagePath(Model):
    # FIXME: refactor on_delete
    parent = ForeignKey('self', on_delete=CASCADE, blank=True, null=True)
    path = CharField(max_length=256, blank=False, null=False, unique=True)

    def _get_full_path(self):
        return join(self.parent.full_path if self.parent else '', self.path)

    full_path = property(_get_full_path)

    def save(self, *args, **kwargs):
        is_saved = self.pk is not None
        super(ImagePath, self).save(*args, **kwargs)
        if not is_saved and not self.parent:
            root_path, created = RootPath.objects.get_or_create(image_path=self)
            if created:
                root_path.save()

    def __str__(self):
        return self.full_path


class RootPath(Model):
    image_path = OneToOneField(ImagePath, on_delete=CASCADE, primary_key=True)
