from django.forms import ModelForm, CharField, Form, ChoiceField, EmailField
from django.forms.widgets import TextInput, PasswordInput, Textarea
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from backend.models import ImageMetadata, ImagePath
from backend.thumbnail.thumbnail_queue_image_object import ThumbQueueImageObject
from backend.thumbnail.thumbnail_queue import ThumbQueue
from gallery.validators import validate_path_parent, validate_path_name


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
    username = CharField(widget=TextInput(attrs={'placeholder': 'Username', 'class': 'input'}))
    password = CharField(widget=PasswordInput(attrs={'placeholder': 'Password', 'class': 'input'}))


class NewFolderForm(Form):
    pathname = CharField(required=True, validators=[validate_path_parent])
    name = CharField(required=True, validators=[validate_path_name])

    def save(self, commit=True):
        pathname = self.cleaned_data['pathname']
        pathname = pathname[:-1] if pathname[-1] == '/' else pathname
        parents = pathname.split('/')[2:]
        name = self.cleaned_data['name']

        # It is assumed that a parent exists (validated earlier)
        parent = None
        for current in parents:
            parent = ImagePath.objects.get(path=current, parent=parent)

        instance = ImagePath.objects.create(path=name, parent=parent)
        return instance


class DeleteForm(Form):
    object_type_choices = [('image', 'image'), ('folder', 'folder')]

    objectId = CharField(required=True)
    objectType = ChoiceField(choices=object_type_choices, required=True)


class FeedbackForm(Form):
    title = CharField(required=True, widget=TextInput(attrs={'class': 'input', 'type': 'text'}))
    text = CharField(max_length=8192, required=True, widget=Textarea(attrs={'class': 'textarea'}))
    email = EmailField(required=False, widget=TextInput(attrs={'class': 'input', 'type': 'email'}))
