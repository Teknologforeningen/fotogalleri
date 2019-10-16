from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from django.views import View
from django.http import JsonResponse
from backend.models import ImageMetadata, RootImage, ImagePath, RootPath
from gallery.forms import ImageUploadForm, NewFolderForm
from os import sep
from os.path import normpath


class HomeView(View):
    template = 'base.html'

    def get(self, request):
        context = {}
        return render(request, self.template, context)


class ImageGalleryView(ListView):
    model = ImageMetadata
    template = 'view_images.html'

    def get(self, request):
        context = {'object_list': self.model.objects.all()}
        return render(request, self.template, context)


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
        if not request.user.is_superuser:
            return redirect('login')
        return super().dispatch(request)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            image = form.save()
            data = {'is_valid': True, 'name': image.image.name, 'url': image.image.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


class NewFolderView(CreateView):
    model = ImagePath
    form_class = NewFolderForm
    template_name = 'new_folder.html'

    def dispatch(self, request):
        if not request.user.is_superuser:
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
