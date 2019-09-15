from backend.models import ImageMetadata
from backend.thumbnail.thumbnail_utils import generate_thumbnails, save_to_path
from ntpath import split
from os.path import join, splitext
from logging import getLogger


logger = getLogger(__name__)


class _ThumbnailObject():
    def __init__(self, thumbnail):
        self.thumbnail = thumbnail
        self._done = False

    def set_done(self):
        self._done = True

    def is_done(self):
        return self._done

    def get_dimensions(self):
        return self.thumbnail.size


class ThumbQueueImageObject():
    # TODO: defined sizes, perhaps specified in the environment?
    _DEFAULT_MINSIZES = [300]
    _DEFAULT_MAXSIZES = []

    def __init__(self, image_metadata: ImageMetadata):
        self.metadata = image_metadata

    def _create_thumbnail_objects(self):
        return [
            _ThumbnailObject(thumbnail)
            for thumbnail in
            generate_thumbnails(
                self.metadata.image.path,
                ThumbQueueImageObject._DEFAULT_MINSIZES,
                ThumbQueueImageObject._DEFAULT_MAXSIZES)
        ]

    def _init_save_thumbnail(self, filename, path):
        def save_thumbnail(thumbnail_object):
            try:
                save_to_path(thumbnail_object.thumbnail, filename, path)
            # TODO: set specific exception
            except Exception as error:
                logger.error('Could not save thumbnail for {}, reason: {}'.format(thumbnail_object.thumbnail, error))
                return False
            thumbnail_object.set_done()
            return True
        return save_thumbnail

    def _save_thumbnails(self, thumbnail_objects):
        raw_path, raw_filename = self._get_image_name_and_path()
        path = join(raw_path, 'thumbnails')
        filename, _ = splitext(raw_filename)
        save_thumbnail_to_path = self._init_save_thumbnail(filename, path)
        return filter(lambda thumbnail_object: save_thumbnail_to_path(thumbnail_object), thumbnail_objects)

    def generate_thumbnails(self):
        thumbnail_objects = self._create_thumbnail_objects()
        saved_thumbnails = self._save_thumbnails(thumbnail_objects)
        self.metadata.set_thumbnails([saved_thumbnail.get_dimensions() for saved_thumbnail in saved_thumbnails])

    def get_full_image_path(self):
        return self.metadata.image.path

    def _get_image_name_and_path(self):
        '''
        Getter for the filename and path of this image.
        :return: (filename, path)
        '''
        image_path = self.get_full_image_path()
        return split(image_path)

    def __str__(self):
        return self.metadata.__str__()
