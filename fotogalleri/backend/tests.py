from django.test import TestCase
from backend.models import ImageMetadata, RootImage
from backend.models import ImagePath, RootPath
from fotogalleri.settings import BASE_DIR, MEDIA_ROOT
from os.path import join, isfile, exists
from shutil import copyfile


class ImageMetadataTest(TestCase):
    def setUp(self):
        image_path = join(BASE_DIR, 'backend', 'fixtures', 'test.png')
        self.image = ImageMetadata.objects.create(image=image_path)

    def test_setting_thumbnails_succeds(self):
        test_thumbnails = [[25, 25], [40, 40]]
        self.image.set_thumbnails(test_thumbnails)
        self.assertEqual(self.image.thumbnails, test_thumbnails)

    def test_setting_thumbnails_fails(self):
        test_thumbnails = None
        with self.assertRaises(TypeError):
            self.image.set_thumbnails(test_thumbnails)

    def test_root_image(self):
        root_image = RootImage.objects.get(image_metadata=self.image)
        self.assertEqual(root_image.image_metadata, self.image)


class ImagePathTest(TestCase):
    PARENT_PATH = 'parent'
    CHILD_PATH = 'child'

    def setUp(self):
        self.parent = ImagePath.objects.create(path=ImagePathTest.PARENT_PATH)
        self.child = ImagePath.objects.create(parent=self.parent, path=ImagePathTest.CHILD_PATH)

    def test_full_parent_path(self):
        self.assertEqual(self.parent.full_path, ImagePathTest.PARENT_PATH)

    def test_full_child_path(self):
        full_child_path = join(ImagePathTest.PARENT_PATH, ImagePathTest.CHILD_PATH)
        self.assertEqual(self.child.full_path, full_child_path)

    def test_parent_root_path(self):
        root_path = RootPath.objects.get(image_path=self.parent)
        self.assertEqual(root_path.image_path, self.parent)

    def test_child_root_path(self):
        with self.assertRaises(RootPath.DoesNotExist):
            RootPath.objects.get(image_path=self.child)


class ImageMetadataDeleteTest(TestCase):
    def create_test_image(self):
        fixture_image = join(BASE_DIR, 'backend', 'fixtures', 'test.png')
        image_path = join(MEDIA_ROOT, '__test_image.png')
        copyfile(fixture_image, image_path)
        return image_path

    def setUp(self):
        self.image_path = self.create_test_image()
        self.image = ImageMetadata.objects.create(image=self.image_path)

    def test_delete_receiver(self):
        self.assertTrue(isfile(self.image_path))
        self.image.delete()

        self.assertFalse(isfile(self.image_path))
        self.assertFalse(exists(self.image_path))
