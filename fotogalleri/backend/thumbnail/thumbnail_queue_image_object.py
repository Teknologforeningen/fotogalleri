from backend.models import ImageMetadata
from backend.thumbnail.thumbnail_utils import generate_thumbnails, save_to_path
from ntpath import split
import logging


logger = logging.getLogger(__name__)


class _ThumbnailObject():
    def __init__(self, thumbnail):
        self.thumbnail = thumbnail
        self.dimension = thumbnail.size[0]
        self._done = False

    def set_done(self):
        self._done = True

    def is_done(self):
        return self._done


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
                self.metadata.image_path,
                ThumbQueueImageObject._DEFAULT_MINSIZES,
                ThumbQueueImageObject._DEFAULT_MAXSIZES)
        ]

    def _init_save_thumbnail(self, filename, path):
        def save_thumbnail(thumbnail_object):
            try:
                save_to_path(thumbnail_object.thumbnail, filename, path)
            # TODO: set specific exception
            except Exception:
                logger.error('Could not save thumbnail for {}'.format(thumbnail_object.thumbnail))
                return False
            thumbnail_object.set_done()
            return True
        return save_thumbnail

    def _save_thumbnails(self, thumbnail_objects):
        filename, path = self.get_image_name_and_path()
        save_thumbnail_to_path = self._init_save_thumbnail(filename, path)
        return filter(lambda thumbnail_object: save_thumbnail_to_path(thumbnail_object), thumbnail_objects)

    def generate_thumbnails(self):
        thumbnail_objects = self._create_thumbnail_objects()
        saved_thumbnails = self._save_thumbnails(thumbnail_objects)
        self.metadata.set_thumbnails(saved_thumbnails)

    def get_full_image_path(self):
        return self.metadata.image_path.image_url.url

    def _get_image_name_and_path(self):
        '''
        Getter for the filename and path of this image.
        :return: (filename, path)
        '''
        image_path = self.get_full_image_path()
        return split(image_path)

    def __str__(self):
        return self.metadata.__str__()
