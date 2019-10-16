from django.forms import ModelForm, CharField
from django.forms.widgets import TextInput, PasswordInput
from django.contrib.auth.forms import AuthenticationForm
from backend.models import ImageMetadata, ImagePath
from backend.thumbnail.thumbnail_queue_image_object import ThumbQueueImageObject


class ImageUploadForm(ModelForm):
    year = CharField()
    event = CharField()

    class Meta:
        model = ImageMetadata
        fields = ['image']

    def save(self, commit=True):
        instance = super(ImageUploadForm, self).save(commit=False)

        if commit:
            instance.path = self._create_image_path()
            instance.save()
            thumbnail_generator = ThumbQueueImageObject(instance)
            thumbnail_generator.generate_image_thumbnails()

        return instance

    def _get(self, key):
        return self.cleaned_data.get(key)

    def _create_image_path(self):
        year = ImagePath.create(self._get('year'), parent=None) if self._get('year') else None
        event = ImagePath.create(self._get('event'), parent=year) if self._get('event') else None
        return event


class CustomLoginForm(AuthenticationForm):
    username = CharField(widget=TextInput(attrs={'placeholder': 'Username'}))
    password = CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}))


class NewFolderForm(ModelForm):
    class Meta:
        model = ImagePath
        fields = ['path']
