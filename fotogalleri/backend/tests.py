from django.test import TestCase
from backend.models import ImageMetadata
from fotogalleri.settings import PROJECT_DIR
from os.path import join, exists
from os import makedirs


def get_fixture_path(*args):
    return join(PROJECT_DIR, 'fixtures', *args)


class ImageMetadataTest(TestCase):
    test_image_dir_path = get_fixture_path()
    test_image_filename = 'test.png'
    test_image_dim = 512

    def setUp(self):
        self.first_image = ImageMetadata.objects.create(
            input_dirs=ImageMetadataTest.test_image_dir_path, filename=ImageMetadataTest.test_image_filename)

    def test_dimension_properties(self):
        image_metadata = self.second_image
        self.assertEqual(image_metadata.width, ImageMetadataTest.test_image_dim)
        self.assertEqual(image_metadata.height, ImageMetadataTest.test_image_dim)

    def tearDown(self):
        pass
