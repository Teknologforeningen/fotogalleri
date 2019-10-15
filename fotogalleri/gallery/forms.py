from django.forms import ModelForm
from backend.models import ImageMetadata
from backend.thumbnail.thumbnail_queue_image_object import ThumbQueueImageObject


class ImageUploadForm(ModelForm):
    class Meta:
        model = ImageMetadata
        fields = ['year', 'event', 'image']

    def save(self, commit=True):
        instance = super(ImageUploadForm, self).save(commit=False)

        if commit:
            instance.save()
            thumbnail_generator = ThumbQueueImageObject(instance)
            thumbnail_generator.generate_thumbnails()

        return instance
