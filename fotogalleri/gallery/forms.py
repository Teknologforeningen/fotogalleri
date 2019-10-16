from django.forms import ModelForm, CharField
from django.forms.widgets import TextInput, PasswordInput
from django.contrib.auth.forms import AuthenticationForm
from backend.models import ImageMetadata, ImagePath
from backend.thumbnail.thumbnail_queue_image_object import ThumbQueueImageObject


class ImageUploadForm(ModelForm):
    filepath = CharField(required=False)

    class Meta:
        model = ImageMetadata
        fields = ['image']

    def save(self, commit=True):
        instance = super(ImageUploadForm, self).save(commit=False)

        # Hack to save width and height,
        # getting them in the view results in a ValueError
        self.width = instance.image.width
        self.height = instance.image.height

        if commit:
            instance.path = self._create_image_path()
            instance.save()
            thumbnail_generator = ThumbQueueImageObject(instance)
            thumbnail_generator.generate_image_thumbnails()

        return instance

    def _create_image_path(self):
        path = self.cleaned_data.get('filepath')
        parts = [part for part in path.split('/') if part.strip()]

        current = None
        for part in parts:
            sub, _ = ImagePath.objects.get_or_create(path=part, parent=current)
            current = sub

        return current


class CustomLoginForm(AuthenticationForm):
    username = CharField(widget=TextInput(attrs={'placeholder': 'Username'}))
    password = CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}))
