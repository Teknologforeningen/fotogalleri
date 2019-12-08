from django.forms import ModelForm, CharField, Form, ChoiceField
from django.forms.widgets import TextInput, PasswordInput
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from backend.models import ImageMetadata, ImagePath
from backend.thumbnail.thumbnail_queue_image_object import ThumbQueueImageObject
from backend.thumbnail.thumbnail_queue import ThumbQueue


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
            if settings.ENABLE_THUMB_QUEUE:
                self._enqueue_thumbnail(instance)

        return instance

    def _create_image_path(self):
        path = self.cleaned_data.get('filepath')
        parts = [part for part in path.split('/') if part.strip()]

        current = None
        for part in parts:
            sub, _ = ImagePath.objects.get_or_create(path=part, parent=current)
            current = sub

        return current

    def _enqueue_thumbnail(self, instance):
        thumbnail_generator = ThumbQueueImageObject(instance)
        ThumbQueue.add_image_obj(thumbnail_generator)


class CustomLoginForm(AuthenticationForm):
    username = CharField(widget=TextInput(attrs={'placeholder': 'Username'}))
    password = CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}))


class NewFolderForm(ModelForm):
    class Meta:
        model = ImagePath
        fields = ['path']


class DeleteForm(Form):
    object_type_choices = [('image', 'image'), ('folder', 'folder')]

    objectId = CharField(required=True)
    objectType = ChoiceField(choices=object_type_choices, required=True)
