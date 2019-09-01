from django.forms import ModelForm
from backend.models import ImageMetadata
<<<<<<< HEAD
from backend.thumbnail.thumbnail_queue_image_object import ThumbQueueImageObject
=======
>>>>>>> Temporarily save everything


class ImageUploadForm(ModelForm):
    class Meta:
        model = ImageMetadata
        fields = ['filename', 'image']

<<<<<<< HEAD
    def save(self, commit=True):
        instance = super(ImageUploadForm, self).save(commit=False)

        if commit:
            instance.save()
            thumbnail_generator = ThumbQueueImageObject(instance)
            thumbnail_generator.generate_thumbnails()

        return instance
=======
    def save(self):
        print('INSTANCE', self.instance)
        return self.instance
>>>>>>> Temporarily save everything
