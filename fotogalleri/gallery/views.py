from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DeleteView
from django.views import View
from django.http import JsonResponse
from backend.models import ImageMetadata, RootImage, ImagePath, RootPath
from gallery.forms import ImageUploadForm, NewFolderForm, DeleteForm
from os import sep
from os.path import normpath
from gallery.featuregates import AlphaGate


class HomeView(View):
    template = 'landing_page.html'

    def get(self, request):
        context = {
            'logged_in': request.user.is_authenticated
        }
        return render(request, self.template, context)


class ImageGalleryView(AlphaGate, ListView):
    model = ImageMetadata
    template = 'view_images.html'
    context = {}

    def dispatch(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        self.context = {'is_admin': _is_admin(request.user)}
        return super().dispatch(request)

    def _render_root(self, request):
        root_children = RootPath.objects.all()
        root_images = RootImage.objects.all()
        self.context['folders'] = [path.image_path for path in root_children]
        self.context['images'] = [image.image_metadata for image in root_images]
        return render(request, self.template, self.context)

    def _render_path(self, request, parts):
        root_name = parts[0]
        root = get_object_or_404(RootPath, image_path__path=root_name)

        current = root.image_path
        for part in parts[1:]:
            child = get_object_or_404(ImagePath, parent=current, path=part)
            current = child

        folders = ImagePath.objects.filter(parent=current)
        images = ImageMetadata.objects.filter(path=current)

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


class ImageView(AlphaGate, View):
    template = 'image.html'
    model = ImageMetadata

    def dispatch(self, request, img_id):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, img_id)

    def get(self, request, img_id):
        context = {'image': self.model.objects.get(pk=img_id)}
        return render(request, self.template, context)


class ImageUploadView(AlphaGate, CreateView):
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


class NewFolderView(AlphaGate, CreateView):
    model = ImagePath
    form_class = NewFolderForm
    template_name = 'new_path.html'

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
            data = {'is_valid': False}
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
        deleted = self._delete_object(object_id, object_type)

        data = {'success': is_form_valid and deleted, 'objectId': object_id}
        return JsonResponse(data)

    def _delete_object(self, object_id, object_type):
        if object_type == 'image':
            return ImageMetadata.objects.get(pk=object_id).delete()
        return False


def _is_admin(user):
    return user.is_staff or user.is_superuser
