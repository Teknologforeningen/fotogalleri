from backend.models import ImageMetadata
from backend.thumbnail.thumbnail_utils import generate_thumbnails, save_to_path
from ntpath import split


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
    _DEFAULT_MINSIZES = []
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

    def _save_thumbnails(self, thumbnail_objects):
        filename, path = self.get_image_name_and_path()
        for thumbnail_object in thumbnail_objects:
            save_to_path(thumbnail_object.thumbnail, filename, path)
            thumbnail_object.set_done()

    def generate_thumbnails(self):
        thumbnail_objects = self._create_thumbnail_objects()
        self._save_thumbnails(thumbnail_objects)

    def get_full_image_path(self):
        return self.metadata.image_path.image_url.url

    def _get_image_name_and_path(self):
        '''
        Getter for the filename and path of this image.
        :return: (filename, path)
        '''
        image_path = self.get_full_image_path()
        return split(image_path)
