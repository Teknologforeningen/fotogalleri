from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DeleteView
from django.views import View
from django.http import JsonResponse
from django.conf import settings
from backend.models import ImageMetadata, RootImage, ImagePath, RootPath
from gallery.forms import ImageUploadForm, NewFolderForm, DeleteForm, FeedbackForm
from os import sep
from os.path import normpath
from gallery.mailutils import mail_feedback


class HomeView(View):
    def get(self, request):
        return redirect('/view/')


class ImageGalleryView(ListView):
    model = ImageMetadata
    template = 'view_images.html'
    context = {}

    def dispatch(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        self.context = {'is_admin': _is_admin(request.user)}
        return super().dispatch(request)

    def _exclude_hidden(self, object_list):
        return [object for object in object_list if not object.hidden]

    def _render_root(self, request):
        root_children = RootPath.objects.all().order_by('image_path__path')
        root_images = RootImage.objects.all().order_by('image_metadata__image')
        folders = [path.image_path for path in root_children]
        images = [image.image_metadata for image in root_images]

        if not self.context['is_admin']:
            folders = self._exclude_hidden(folders)
            images = self._exclude_hidden(images)

        self.context['folders'] = folders
        self.context['images'] = images
        return render(request, self.template, self.context)

    def _render_path(self, request, parts):
        root_name = parts[0]
        root = get_object_or_404(RootPath, image_path__path=root_name)

        current = root.image_path
        for part in parts[1:]:
            child = get_object_or_404(ImagePath, parent=current, path=part)
            current = child

        folders = ImagePath.objects.filter(parent=current).order_by('path')
        images = ImageMetadata.objects.filter(path=current).order_by('image')

        if not self.context['is_admin']:
            folders = self._exclude_hidden(folders)
            images = self._exclude_hidden(images)

        self.context['folder'] = current
        self.context['folders'] = folders
        self.context['images'] = images
        return render(request, self.template, self.context)

    def get(self, request):
        full_url_path = request.get_full_path()
        path = normpath(full_url_path)
        parts = path.split(sep)

        cleaned_parts = [part for part in parts if part.strip() and part != 'view']
        if not cleaned_parts:  # User queries for root
            return self._render_root(request)
        else:
            return self._render_path(request, cleaned_parts)


class ImageView(View):
    template = 'image.html'
    model = ImageMetadata

    def dispatch(self, request, img_id):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, img_id)

    def get(self, request, img_id):
        context = {'image': self.model.objects.get(pk=img_id)}
        return render(request, self.template, context)


class ImageUploadView(CreateView):
    model = ImageMetadata
    form_class = ImageUploadForm
    template_name = 'upload_image.html'

    def dispatch(self, request):
        if not _is_admin(request.user):
            return redirect('login')
        return super().dispatch(request)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            image = form.save()
            data = {
                'is_valid': True,
                'name': image.image.name,
                'url': image.image.url,
                'width': form.width,
                'height': form.height,
            }
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


class NewFolderView(CreateView):
    model = ImagePath
    form_class = NewFolderForm

    def dispatch(self, request):
        if not _is_admin(request.user):
            return redirect('login')
        return super().dispatch(request)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            path = form.save()
            data = {
                'is_valid': True,
                'path': path.path,
                'full_path': path.full_path,
            }
        else:
            data = {
                'is_valid': False,
                'error_msg': list(form.errors.values())
            }
        return JsonResponse(data)


class DeleteObject(DeleteView):
    form_class = DeleteForm

    def dispatch(self, request):
        if not _is_admin(request.user):
            return redirect('login')
        return super().dispatch(request)

    def post(self, request, *args, **kwargs):
        form = DeleteForm(request.POST)
        is_form_valid = form.is_valid()

        object_id = form.cleaned_data['objectId']
        object_type = form.cleaned_data['objectType']

        try:
            self._delete_object(object_id, object_type)
        except Exception as error:
            data = {
                'success': False,
                'objectId': object_id,
                'errorMessage': str(error)
            }
        else:
            data = {
                'success': is_form_valid,
                'objectId': object_id
            }

        return JsonResponse(data)

    def _delete_object(self, object_id, object_type):
        if object_type == 'image':
            ImageMetadata.objects.get(pk=object_id).delete()
        elif object_type == 'folder':
            path = ImagePath.objects.get(pk=object_id)
            if not path.is_empty:
                raise Exception('Only empty folders can be deleted.')
            path.delete()


class Feedback(View):
    form_class = FeedbackForm
    template = 'feedback.html'

    def dispatch(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        self.context = {
            'email': settings.FEEDBACK_EMAIL_RECEIVER
        }
        return super().dispatch(request)

    def get(self, request):
        self.context['form'] = self.form_class
        return render(request, self.template, self.context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            self.context['thanks'] = True
            mail_feedback(form.cleaned_data)
            self.context['form'] = self.form_class
            return render(request, self.template, self.context)
        else:
            self.context['form'] = form
            return render(request, self.template, self.context, status=400)


def _is_admin(user):
    return user.is_staff or user.is_superuser
