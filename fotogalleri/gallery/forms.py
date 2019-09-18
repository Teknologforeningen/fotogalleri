from django.forms import ModelForm
from backend.models import ImageMetadata


class ImageUploadForm(ModelForm):
    class Meta:
        model = ImageMetadata
        fields = ['filename', 'image']
