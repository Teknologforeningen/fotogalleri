from django.forms import ModelForm, CharField
from django.forms.widgets import TextInput, PasswordInput
from django.contrib.auth.forms import AuthenticationForm
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
            thumbnail_generator.generate_image_thumbnails()

        return instance


class CustomLoginForm(AuthenticationForm):
    username = CharField(widget=TextInput(attrs={'placeholder': 'Username'}))
    password = CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}))
