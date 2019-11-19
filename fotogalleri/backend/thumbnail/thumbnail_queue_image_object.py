from django.conf import settings
from backend.thumbnail.thumbnail_utils import generate_thumbnails, save_img_to_path
from ntpath import split
from os.path import join, splitext
from logging import getLogger


logger = getLogger(__name__)


class ThumbQueueImageObject():
    # TODO: defined sizes, perhaps specified in the environment?
    _DEFAULT_MINSIZES = [300]
    _DEFAULT_MAXSIZES = []

    def __init__(self, image_metadata):
        self.metadata = image_metadata

    def _create_thumbnail_objects(self):
        return [
            thumbnail
            for thumbnail in
            generate_thumbnails(
                self.metadata.image.path,
                ThumbQueueImageObject._DEFAULT_MINSIZES,
                ThumbQueueImageObject._DEFAULT_MAXSIZES)
        ]

    def _init_save_thumbnail(self, filename, path):
        def save_thumbnail(thumbnail_object):
            try:
                save_img_to_path(thumbnail_object, filename, path)
            # TODO: set specific exception
            except Exception as error:
                logger.error('Could not save thumbnail for {}, reason: {}'.format(thumbnail_object.thumbnail, error))
                return False
            return True
        return save_thumbnail

    def _save_thumbnails(self, thumbnail_objects):
        raw_path, raw_filename = self._get_image_path_and_name()
        path = join(raw_path, settings.THUMBNAILS_NAME)
        filename, _ = splitext(raw_filename)
        save_thumbnail_to_path = self._init_save_thumbnail(filename, path)
        return filter(lambda thumbnail_object: save_thumbnail_to_path(thumbnail_object), thumbnail_objects)

    def generate_image_thumbnails(self):
        thumbnail_objects = self._create_thumbnail_objects()
        saved_thumbnails = self._save_thumbnails(thumbnail_objects)
        self.metadata.set_thumbnails([saved_thumbnail.size for saved_thumbnail in saved_thumbnails])

    def get_full_image_path(self):
        return self.metadata.image.path

    def _get_image_path_and_name(self):
        '''
        Getter for the filename and path of this image.
        :return: (path, filename)
        '''
        image_path = self.get_full_image_path()
        return split(image_path)

    def __str__(self):
        return self.metadata.__str__()
